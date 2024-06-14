from django.shortcuts import render
from django.db.models import Sum
from drive.models import File, Folder
from django.db import models


# Create your views here.

def drive(request):


    folder_list = Folder.objects.all()
    file_list = File.objects.all()
    folder_number = Folder.objects.count()
    file_number = File.objects.count()
    used_quota_bytes = File.objects.all().aggregate(total_size=models.Sum('file_size'))['total_size'] or 0
    used_quota_mbs = round(used_quota_bytes / (1024 * 1024), 2)

    context = {
        'folder_list': folder_list,
        'file_list': file_list,
        'used_quota': f"{used_quota_mbs} MB",
        "folder_number": folder_number,
        "file_number": file_number,
    }


    # Render the HTML template index.html with the data in the context variable
    return render(request, 'drive.html', context=context)
