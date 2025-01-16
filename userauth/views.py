from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import Group

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('home')  # Redirect to the home page or any desired page
    else:
        form = CustomUserCreationForm()
    return render(request, 'userauth/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page
    else:
        form = CustomAuthenticationForm()
    return render(request, 'userauth/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'userauth/home.html')

# Create your views here.
