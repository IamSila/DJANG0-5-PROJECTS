from django.urls import path
from . import views
from .views import MemberExportView

urlpatterns = [
  path('home/', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('members/', views.members, name='members'),
  path('classes/', views.classes, name='classes'),
  path('trainers/', views.trainers, name='trainers'),
  path('payments/', views.payments, name='payments'),
  path('reports/', views.reports, name='reports'),
  path('personalised-training/', views.personalised_training, name='personalised_training'),
  path('export_members/', MemberExportView.as_view(), name='export_members'),
  path("members_upload/", views.member_upload_file, name='member_upload'),
]
