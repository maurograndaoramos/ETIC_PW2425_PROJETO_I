from django.shortcuts import render

def landing_page(request):
    return render(request, 'Edrive/landing-page.html')

