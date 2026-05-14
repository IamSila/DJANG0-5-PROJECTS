from django.urls import path
from . import views


urlpatterns = [
  path('home/', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('members/', views.members, name='members'),
  path('classes/', views.classes, name='classes'),
  path('trainers/', views.trainers, name='trainers'),
  path('payments/', views.payments, name='payments'),
  path('reports/', views.reports, name='reports'),
  path('personalised-training/', views.personalised_training, name='personalised_training'),
  path('members/export_members/', views.members, name='export_members'),
  path("members/import_members/", views.members, name='import_members'),
  path('members/addMember/', views.add_member, name='add_member'),
]
