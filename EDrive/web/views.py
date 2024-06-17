from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def premium(request):
    return render(request, 'premium.html')

class SignupView(FormView):
    template_name="auth/signup.html"
    form_class=UserCreationForm
    success_url=reverse_lazy('login')
    redirect_authenticated_user = True

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(SignupView,self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts')
        return super(SignupView,self).get(request, *args, **kwargs)


class Login(LoginView):
    template_name="auth/login.html"
    fields= "__all__"
    redirect_authenticated_user = True
    success_url = "posts"
