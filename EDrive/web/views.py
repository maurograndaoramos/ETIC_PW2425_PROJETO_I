from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

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
    return render(request, 'auth/signup.html', {'form': form})

class Login(LoginView):
    template_name="auth/login.html"
    fields= "__all__"
    redirect_authenticated_user = True
    success_url = "posts"

class Logout(LogoutView):
    next_page = reverse_lazy('home')

