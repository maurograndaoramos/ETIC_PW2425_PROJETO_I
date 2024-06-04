from django.shortcuts import render, redirect
from django.contrib.auth import login
from . import RegisterForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('file_management.view_files', raise_exception=True)
def file_list(request):
    # Logic for listing files
    pass


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})
