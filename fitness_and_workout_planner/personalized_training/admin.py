from django.contrib import admin
from .models import UserProfile, PlannedWorkout, WorkoutLog, Goal, TrainerTip

admin.site.register(UserProfile)
admin.site.register(PlannedWorkout)
admin.site.register(WorkoutLog)
admin.site.register(Goal)
admin.site.register(TrainerTip)