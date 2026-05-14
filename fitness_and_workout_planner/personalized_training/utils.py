from datetime import date, timedelta
from django.utils import timezone
from .models import PlannedWorkout, WorkoutLog
from django.db.models import Sum

def get_exercises_for_workout(workout_type, goal):
    """Return a string of exercises based on workout type and user's goal"""
    exercises_map = {
        ('cardio', 'weight_loss'): "Running, Cycling, Jump Rope, Burpees",
        ('cardio', 'muscle_gain'): "Sprints, Rowing Machine, Battle Ropes",
        ('cardio', 'endurance'): "Long-distance running, Swimming, Cycling intervals",
        ('cardio', 'flexibility'): "Dynamic stretching, Walking lunges, Light jogging",
        ('strength', 'weight_loss'): "Push-ups, Squats, Deadlifts, Lunges, Pull-ups",
        ('strength', 'muscle_gain'): "Bench Press, Rows, Overhead Press, Deadlifts, Pull-ups",
        ('strength', 'endurance'): "Circuit training: Push-ups, Squats, Lunges, Planks",
        ('strength', 'flexibility'): "Bodyweight squats, Light resistance band work",
        ('yoga', 'weight_loss'): "Power Yoga, Sun Salutations, Warrior sequences",
        ('yoga', 'muscle_gain'): "Ashtanga, Arm balances, Core-focused flows",
        ('yoga', 'endurance'): "Vinyasa flow, Sun Salutations, Standing poses",
        ('yoga', 'flexibility'): "Yin Yoga, Deep stretching, Hatha Yoga",
        ('hiit', 'weight_loss'): "Burpees, Mountain Climbers, Jump Squats, High Knees",
        ('hiit', 'muscle_gain'): "Kettlebell swings, Box jumps, Battle ropes",
        ('hiit', 'endurance'): "Tabata: Sprints, Rowing intervals",
        ('hiit', 'flexibility'): "Low-impact HIIT: Lateral shuffles, Step-ups",
        ('recovery', 'weight_loss'): "Walking, Light stretching, Foam rolling",
        ('recovery', 'muscle_gain'): "Active recovery swim, Light mobility work",
        ('recovery', 'endurance'): "Easy cycling, Stretching routine",
        ('recovery', 'flexibility'): "Full body stretching, Yoga Nidra",
    }
    return exercises_map.get((workout_type, goal), "Consult your trainer for personalized exercises")


def generate_weekly_schedule(user):
    """Generate planned workouts for the next 7 days based on user profile"""
    profile = user.userprofile
    today = timezone.now().date()
    
    # Get frequency multiplier
    freq_map = {'1-2': 2, '3-4': 3.5, '5-6': 5, '7': 7}
    workouts_per_week = int(freq_map.get(profile.workout_frequency, 3.5))
    
    # Distribute workout days (simple: first N days of the week)
    workout_days = []
    for i in range(7):
        if len(workout_days) < workouts_per_week:
            workout_days.append(i)
    
    # Types of workouts based on goal
    goal = profile.primary_goal
    workout_rotation = []
    if goal == 'weight_loss':
        workout_rotation = ['cardio', 'strength', 'hiit', 'cardio', 'strength', 'hiit', 'recovery']
    elif goal == 'muscle_gain':
        workout_rotation = ['strength', 'strength', 'cardio', 'strength', 'strength', 'recovery', 'rest']
    elif goal == 'endurance':
        workout_rotation = ['cardio', 'strength', 'cardio', 'hiit', 'cardio', 'recovery', 'rest']
    else:  # flexibility
        workout_rotation = ['yoga', 'cardio', 'yoga', 'strength', 'yoga', 'recovery', 'rest']
    
    # Create or update planned workouts for next 7 days
    for day_offset in range(7):
        workout_date = today + timedelta(days=day_offset)
        day_index = workout_date.weekday()  # Monday=0, Sunday=6
        
        # Determine workout type (use rotation or rest if not a workout day)
        if day_index in workout_days and day_offset < len(workout_rotation):
            workout_type = workout_rotation[day_offset]
        else:
            workout_type = 'rest' if day_index not in workout_days else 'recovery'
        
        # Set duration and intensity
        intensity_map = {
            'cardio': ('medium', 45),
            'strength': ('high', 60),
            'yoga': ('low', 30),
            'hiit': ('very high', 40),
            'recovery': ('low', 20),
            'rest': ('rest', 0)
        }
        intensity, duration = intensity_map.get(workout_type, ('medium', 45))
        
        exercises = get_exercises_for_workout(workout_type, goal) if workout_type != 'rest' else "Rest and recovery"
        
        planned, created = PlannedWorkout.objects.update_or_create(
            user=user,
            date=workout_date,
            defaults={
                'workout_type': workout_type,
                'exercises': exercises,
                'duration': duration,
                'intensity': intensity,
            }
        )


def update_user_stats(user):
    """Update profile stats based on workout logs"""
    profile = user.userprofile
    logs = WorkoutLog.objects.filter(user=user)
    
    total_workouts = logs.count()
    total_minutes = logs.aggregate(total=Sum('duration'))['total'] or 0
    total_calories = logs.aggregate(total=Sum('calories'))['total'] or 0
    
    profile.total_workouts = total_workouts
    profile.total_hours = round(total_minutes / 60, 1)
    profile.calories_burned = total_calories
    
    # Calculate current streak
    today = timezone.now().date()
    streak = 0
    check_date = today
    while WorkoutLog.objects.filter(user=user, date=check_date).exists():
        streak += 1
        check_date -= timedelta(days=1)
    profile.current_streak = streak
    
    if streak > profile.best_streak:
        profile.best_streak = streak
    
    # Calculate goal progress (simplified)
    if profile.starting_weight and profile.goal_weight and profile.weight:
        total_loss_needed = profile.starting_weight - profile.goal_weight
        if total_loss_needed > 0:
            lost_so_far = profile.starting_weight - profile.weight
            progress = int((lost_so_far / total_loss_needed) * 100)
            profile.goal_progress = min(100, max(0, progress))
    
    profile.save()


def get_recent_workouts(user, limit=5):
    return WorkoutLog.objects.filter(user=user).order_by('-date')[:limit]