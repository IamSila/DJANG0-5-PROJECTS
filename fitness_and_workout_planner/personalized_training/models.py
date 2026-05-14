from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    FITNESS_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
    ]
    FREQUENCY_CHOICES = [
        ('1-2', '1-2 times per week'),
        ('3-4', '3-4 times per week'),
        ('5-6', '5-6 times per week'),
        ('7', 'Daily'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVELS, default='intermediate')
    primary_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='weight_loss')
    workout_frequency = models.CharField(max_length=5, choices=FREQUENCY_CHOICES, default='3-4')
    body_fat = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True, help_text="Muscle mass in kg")
    starting_weight = models.FloatField(null=True, blank=True)
    goal_weight = models.FloatField(null=True, blank=True)
    
    # Membership & trainer info
    membership_type = models.CharField(max_length=50, default='Premium')
    membership_expiry = models.DateField(default=timezone.now() + timedelta(days=365))
    trainer_name = models.CharField(max_length=100, default='Lisa Wilson')
    next_session = models.CharField(max_length=100, default='Next session: Tomorrow')
    
    # Stats
    current_streak = models.IntegerField(default=0)
    total_workouts = models.IntegerField(default=0)
    total_hours = models.FloatField(default=0.0)
    calories_burned = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    goal_progress = models.IntegerField(default=0)  # percentage
    
    # Nutrition targets (auto-calculated)
    daily_calories = models.IntegerField(default=2200)
    protein_goal = models.IntegerField(default=150)
    carbs_goal = models.IntegerField(default=250)
    fats_goal = models.IntegerField(default=70)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None
    
    def update_nutrition_targets(self):
        """Calculate daily calorie and macro needs based on goal and weight"""
        # BMR using Mifflin-St Jeor (simplified)
        if self.age and self.weight and self.height:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age
            if self.user.profile.gender == 'male':
                bmr += 5
            else:
                bmr -= 161
        else:
            bmr = 2000
        
        # Adjust for activity level
        activity_multiplier = 1.375  # light activity default
        if self.workout_frequency == '1-2':
            activity_multiplier = 1.2
        elif self.workout_frequency == '3-4':
            activity_multiplier = 1.375
        elif self.workout_frequency == '5-6':
            activity_multiplier = 1.55
        elif self.workout_frequency == '7':
            activity_multiplier = 1.725
        
        maintenance = bmr * activity_multiplier
        
        if self.primary_goal == 'weight_loss':
            self.daily_calories = int(maintenance - 500)
            self.protein_goal = int(self.weight * 2.2)  # 2.2g per kg
            self.carbs_goal = int(self.daily_calories * 0.4 / 4)
            self.fats_goal = int(self.daily_calories * 0.25 / 9)
        elif self.primary_goal == 'muscle_gain':
            self.daily_calories = int(maintenance + 300)
            self.protein_goal = int(self.weight * 2.5)
            self.carbs_goal = int(self.daily_calories * 0.5 / 4)
            self.fats_goal = int(self.daily_calories * 0.2 / 9)
        else:  # endurance or flexibility
            self.daily_calories = int(maintenance)
            self.protein_goal = int(self.weight * 1.8)
            self.carbs_goal = int(self.daily_calories * 0.55 / 4)
            self.fats_goal = int(self.daily_calories * 0.2 / 9)
        
        self.save()
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class PlannedWorkout(models.Model):
    WORKOUT_TYPES = [
        ('cardio', 'Cardio & Endurance'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga & Flexibility'),
        ('hiit', 'HIIT Training'),
        ('recovery', 'Active Recovery'),
        ('rest', 'Rest Day'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planned_workouts')
    date = models.DateField()
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    exercises = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    intensity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('very high', 'Very High')])
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['date']
    
    @property
    def day_name(self):
        return self.date.strftime('%A')
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.workout_type}"


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    date = models.DateField(default=timezone.now)
    workout_type = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Minutes")
    calories = models.IntegerField()
    intensity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.workout_type}"


class Goal(models.Model):
    GOAL_TYPES = [
        ('weight', 'Weight Goal'),
        ('workout', 'Workout Frequency'),
        ('strength', 'Strength Goal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_value = models.CharField(max_length=50)
    current_value = models.CharField(max_length=50, blank=True)
    deadline = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.goal_type}"


class TrainerTip(models.Model):
    tip_text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.tip_text
