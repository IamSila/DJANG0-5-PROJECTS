from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
#  path('login/', views.user_login, name='login'),
  #login and logout view using detault django auth
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
