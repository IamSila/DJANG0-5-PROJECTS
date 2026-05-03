from django.shortcuts import render
# utils
from django.utils import timezone
# models
from .models import Member
# Create your views here.



# home page
def home(request):
  context = {}
  return render(request, 'mainApp/base.html', context)


# dashboard page
def dashboard(request):
  context = {}
  return render(request, 'mainApp/dashboard.html', context)


# members page
def members(request):
  members = Member.objects.all()

  # statistics
  total_members = Member.objects.count()
  active_members = Member.objects.filter(status='ACTIVE').count()
  now = timezone.now()
  new_this_month = Member.objects.filter(join_date__month = now.month).count()

  context = {"members":members, "total_members": total_members, "active_members": active_members, "new_this_month": new_this_month}
  return render(request, 'mainApp/members.html', context)



# classes page
def classes(request):
  context = {}
  return render(request, 'mainApp/classes.html', context)

# trainers page
def trainers(request):
  context = {}
  return render(request, 'mainApp/trainers.html', context)

# payments page
def payments(request):
  context = {}
  return render(request, 'mainApp/payments.html', context)

# report page
def reports(request):
  context = {}
  return render(request, 'mainApp/reports.html', context)