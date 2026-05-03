from django.shortcuts import render
# utils
from django.utils import timezone
# models
from .models import Member
# Create your views here.



# home page
def home(request):
  context = {}
  return render(request, 'mainApp/base.html', context)


# dashboard page
def dashboard(request):
  members = Member.objects.all()

  # statistics
  total_members = Member.objects.count()
  active_members = Member.objects.filter(status='ACTIVE').count()
  now = timezone.now()
  new_this_month = Member.objects.filter(join_date__month = now.month).count()

  context = {"members":members, "total_members": total_members, "active_members": active_members, "new_this_month": new_this_month}
  return render(request, 'mainApp/dashboard.html', context)


# members page
def members(request):
  members = Member.objects.all()

  # statistics
  total_members = Member.objects.count()
  active_members = Member.objects.filter(status='ACTIVE').count()
  now = timezone.now()
  new_this_month = Member.objects.filter(join_date__month = now.month).count()

  context = {"members":members, "total_members": total_members, "active_members": active_members, "new_this_month": new_this_month}
  return render(request, 'mainApp/members.html', context)



# classes page
def classes(request):
  context = {}
  return render(request, 'mainApp/classes.html', context)

# trainers page
def trainers(request):
  context = {}
  return render(request, 'mainApp/trainers.html', context)

# payments page
def payments(request):
  context = {}
  return render(request, 'mainApp/payments.html', context)

# report page
def reports(request):
  context = {}
  return render(request, 'mainApp/reports.html', context)


def personalised_training(request):
    # Get member_id from session or URL parameter
    member_id = request.GET.get('member_id', 1)
    
    # This data would normally come from your database
    context = {
        'member': {
            'first_name': 'John',
            'membership_type': 'Premium',
            'membership_expiry': 'Dec 31, 2024',
            'fitness_level': 'Intermediate',
            'assessment_date': '2024-01-01',
            'primary_goal': 'Weight Loss',
            'goal_progress': 65,
            'trainer_name': 'Lisa Wilson',
            'next_session': 'Tomorrow, 10:00 AM',
            'current_weight': 165,
            'starting_weight': 175,
            'weight_loss': 10,
            'goal_weight': 155,
            'body_fat': 22,
            'starting_body_fat': 26,
            'body_fat_loss': 4,
            'muscle_mass': 72,
            'starting_muscle': 68,
            'muscle_gain': 4,
            'current_streak': 5,
            'best_streak': 12,
            'total_workouts': 28,
            'total_hours': 42.5,
            'calories_burned': 12450,
            'daily_calories': 2200,
            'protein_goal': 150,
            'carbs_goal': 250,
            'fats_goal': 70,
            'early_workouts': 15,
            'strength_workouts': 8,
            'workouts_last_30_days': 18,
            'calories_last_30_days': 8450,
            'weight_last_30_days': 3.5,
            'strength_increase': 15,
            'consistency_rate': 75,
            'trainer_feedback': 'Great progress! Keep up the consistency. Focus on increasing your protein intake for better recovery.'
        },
        'weekly_workouts': [
            {'day': 'Monday', 'type': 'Cardio & Endurance', 'exercises': 'Running, Cycling, Jump Rope', 'duration': 45, 'intensity': 'Medium', 'completed': False},
            {'day': 'Tuesday', 'type': 'Strength Training', 'exercises': 'Push-ups, Squats, Deadlifts', 'duration': 60, 'intensity': 'High', 'completed': False},
            {'day': 'Wednesday', 'type': 'Yoga & Flexibility', 'exercises': 'Sun Salutations, Stretching', 'duration': 30, 'intensity': 'Low', 'completed': False},
            {'day': 'Thursday', 'type': 'HIIT Training', 'exercises': 'Burpees, Mountain Climbers', 'duration': 40, 'intensity': 'Very High', 'completed': False},
            {'day': 'Friday', 'type': 'Strength Training', 'exercises': 'Bench Press, Rows, Pull-ups', 'duration': 60, 'intensity': 'High', 'completed': False},
            {'day': 'Saturday', 'type': 'Active Recovery', 'exercises': 'Walking, Light Stretching', 'duration': 20, 'intensity': 'Low', 'completed': False},
            {'day': 'Sunday', 'type': 'Rest Day', 'exercises': 'Recovery & Meal Prep', 'duration': 0, 'intensity': 'Rest', 'completed': True},
        ],
        'recent_workouts': [
            {'date': '2024-01-15', 'type': 'Strength Training', 'duration': 60, 'calories': 450},
            {'date': '2024-01-14', 'type': 'Cardio', 'duration': 45, 'calories': 380},
            {'date': '2024-01-13', 'type': 'Yoga', 'duration': 30, 'calories': 150},
        ]
    }
    return render(request, 'mainApp/personalised_training.html', context)