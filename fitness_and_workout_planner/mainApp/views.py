from django.shortcuts import render

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
  context = {}
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