from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from datetime import date, timedelta
from django.utils import timezone
from .models import UserProfile, PlannedWorkout, WorkoutLog, Goal, TrainerTip
from .forms import AssessmentForm, GoalForm, WorkoutLogForm
from .utils import generate_weekly_schedule, update_user_stats, get_recent_workouts
from django.db.models import Sum

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render

@login_required
def personalized_training(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Generate weekly schedule if not exists for upcoming days
    today = timezone.now().date()
    upcoming_exists = PlannedWorkout.objects.filter(user=user, date__gte=today).exists()
    if not upcoming_exists:
        generate_weekly_schedule(user)
    
    # Get next 7 days of planned workouts
    end_date = today + timedelta(days=7)
    weekly_workouts = PlannedWorkout.objects.filter(
        user=user, date__gte=today, date__lt=end_date
    ).order_by('date')
    
    # Fill missing days in the list for template (ensure 7 days)
    workouts_by_day = {}
    for w in weekly_workouts:
        workouts_by_day[w.date] = w
    
    full_week = []
    for i in range(7):
        d = today + timedelta(days=i)
        if d in workouts_by_day:
            full_week.append(workouts_by_day[d])
        else:
            # Create a placeholder rest day if missing
            planned, _ = PlannedWorkout.objects.get_or_create(
                user=user, date=d,
                defaults={
                    'workout_type': 'rest',
                    'exercises': 'Rest and recovery',
                    'duration': 0,
                    'intensity': 'rest',
                }
            )
            full_week.append(planned)
    
    # Recent logs
    recent_logs = get_recent_workouts(user)
    
    # Get trainer tips
    trainer_tips = TrainerTip.objects.filter(active=True)[:4]
    
    # Calculate additional stats for template
    thirty_days_ago = today - timedelta(days=30)
    last_30_logs = WorkoutLog.objects.filter(user=user, date__gte=thirty_days_ago)
    workouts_last_30 = last_30_logs.count()
    calories_last_30 = last_30_logs.aggregate(total=Sum('calories'))['total'] or 0
    
    # Weight change in last 30 days (simplified - compare latest weight vs weight 30 days ago)
    weight_last_30 = None
    if profile.starting_weight and profile.weight:
        weight_last_30 = profile.weight - (profile.starting_weight or profile.weight)
    
    consistency_rate = 0
    if workouts_last_30 > 0:
        consistency_rate = int((workouts_last_30 / 30) * 100)
    
    context = {
        'member': profile,
        'weekly_workouts': full_week,
        'recent_workouts': recent_logs,
        'trainer_tips': trainer_tips,
        'workouts_last_30_days': workouts_last_30,
        'calories_last_30_days': calories_last_30,
        'weight_last_30_days': abs(weight_last_30) if weight_last_30 and weight_last_30 < 0 else weight_last_30,
        'strength_increase': 15,  # Placeholder - can be calculated from strength logs
        'consistency_rate': consistency_rate,
        'trainer_feedback': "Great progress! Keep up the consistency. Focus on your nutrition for better results.",
    }
    return render(request, 'mainApp/personalized_training.html', context)


@login_required
def assessment_submit(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            profile = form.save()
            # Regenerate schedule with new fitness level/goal
            generate_weekly_schedule(request.user)
            return JsonResponse({'success': True, 'message': 'Assessment submitted successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def goal_submit(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return JsonResponse({'success': True, 'message': 'Goal set successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def workout_log_submit(request):
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            # Update user stats
            update_user_stats(request.user)
            # Mark any planned workout for this day as completed (if matches)
            today = timezone.now().date()
            planned = PlannedWorkout.objects.filter(user=request.user, date=today).first()
            if planned and not planned.completed:
                planned.completed = True
                planned.save()
            return JsonResponse({'success': True, 'message': 'Workout logged successfully! 💪'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def mark_workout_done(request, workout_id):
    if request.method == 'POST':
        planned = get_object_or_404(PlannedWorkout, id=workout_id, user=request.user)
        if not planned.completed:
            planned.completed = True
            planned.save()
            # Also create a workout log entry
            WorkoutLog.objects.create(
                user=request.user,
                date=planned.date,
                workout_type=planned.get_workout_type_display(),
                duration=planned.duration,
                calories=int(planned.duration * 10),  # rough estimate
                intensity=planned.intensity,
                rating=5
            )
            update_user_stats(request.user)
            return JsonResponse({'success': True, 'message': 'Workout marked as done!'})
        return JsonResponse({'success': False, 'message': 'Already completed'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def download_plan(request):
    # Generate a PDF or text file of the user's workout plan
    # For simplicity, return a text response
    user = request.user
    profile = user.userprofile
    upcoming = PlannedWorkout.objects.filter(user=user, date__gte=timezone.now().date()).order_by('date')[:14]
    
    content = f"Personalized Training Plan for {user.username}\n"
    content += f"Goal: {profile.get_primary_goal_display()}\n"
    content += f"Fitness Level: {profile.get_fitness_level_display()}\n\n"
    content += "Upcoming Workouts:\n"
    for workout in upcoming:
        content += f"{workout.date} - {workout.get_workout_type_display()} - {workout.duration} min - {workout.intensity}\n"
        content += f"Exercises: {workout.exercises}\n\n"
    
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="workout_plan.txt"'
    return response



# Use Django's built‑in LoginView (just customize template)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # if already logged in, go to dashboard

    def get_success_url(self):
        return '/personalized-training/'  # redirect after login

class CustomLogoutView(LogoutView):
    next_page = 'login'  # redirect to login page after logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log in after registration
            return redirect('personalized_training')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
