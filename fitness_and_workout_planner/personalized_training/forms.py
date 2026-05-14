from django import forms
from .models import UserProfile, WorkoutLog, Goal

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fitness_level', 'primary_goal', 'weight', 'body_fat', 'workout_frequency', 'age', 'height']
        widgets = {
            'fitness_level': forms.Select(attrs={'class': 'form-control'}),
            'primary_goal': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'body_fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'workout_frequency': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Update nutrition targets after saving
            profile.update_nutrition_targets()
        return profile


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal_type', 'target_value', 'deadline']
        widgets = {
            'goal_type': forms.Select(attrs={'class': 'form-control'}),
            'target_value': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout_type', 'duration', 'calories', 'intensity', 'rating', 'notes']
        widgets = {
            'workout_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'intensity': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }