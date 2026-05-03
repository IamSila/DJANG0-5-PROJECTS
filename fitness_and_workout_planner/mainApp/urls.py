from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('members/', views.members, name='members'),
  path('classes/', views.classes, name='classes'),
  path('trainers/', views.trainers, name='trainers'),
  path('payments/', views.payments, name='payments'),
  path('reports/', views.reports, name='reports')
]
