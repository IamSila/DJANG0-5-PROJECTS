from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('personalized-training/', views.personalized_training, name='personalized_training'),
    path('assessment-submit/', views.assessment_submit, name='assessment_submit'),
    path('goal-submit/', views.goal_submit, name='goal_submit'),
    path('workout-log-submit/', views.workout_log_submit, name='workout_log_submit'),
    path('mark-workout-done/<int:workout_id>/', views.mark_workout_done, name='mark_workout_done'),
    path('download-plan/', views.download_plan, name='download_plan'),
]

