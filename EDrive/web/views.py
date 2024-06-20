from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.urls import reverse_lazy
from .forms import SignUpForm

# Create your views here.

def home(request):

    if request.user.is_authenticated:
        return redirect('drive')
    else:
        return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def premium(request):
    return render(request, 'premium.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('drive')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    if request.user.is_authenticated:
        return redirect('drive')
    else:
        return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('drive')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect('drive')
    else:
        return render(request, 'auth/login.html', {'form': form})      

def password_reset(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
        else:
            print(form.errors)

    else:
        form = SetPasswordForm(request.user)

    if request.user.is_authenticated:
        return redirect('drive')
    else:
        return render(request, 'auth/password_reset_form.html', {'form': form})

class Logout(LogoutView):
    next_page = reverse_lazy('home')

