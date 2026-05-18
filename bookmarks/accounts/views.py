from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.



def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(request, username = cd['username'], password = cd['password'])
      if user is not None:
        if user.is_active:
          login(request, user)
          return JsonResponse({"status": "success", "message": "Action completed."})
        else:
          return JsonResponse({"status": "404 Error", "message": "User Deactivated."})
  else:
    form = LoginForm()

  context = {'form': form}
  return render(request, 'accounts/login.html', context)

