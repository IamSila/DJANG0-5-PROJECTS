from django.urls import path
from . import views

app_name = 'csvs'

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
]