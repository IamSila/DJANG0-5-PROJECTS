from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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


@login_required
def dashboard(request):
  context = {'section': dashboard }
  return render(request, 'accounts/dashboard.html', context)



def register(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
      # create new user object but I avoid saving it
      new_user = user_form.save(commit=False)
      # this set_password is for security: it converts pass to hash
      new_user.set_password(user_form.cleaned_data['password'])
      new_user.save()
  else:
    user_form = UserRegistrationForm()
  context = {'user_form': user_form}
  return render(request, 'account/register.html', context)



