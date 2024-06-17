import os
import zipfile
from django.shortcuts import render,get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from drive.models import File, Folder
from django.db import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone

def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # Assuming you want to upload to the root, file_parent_id will be None or get from request
        file_parent_id = request.POST.get('folder_id', None)
        file_parent = None
        if file_parent_id:
            file_parent = Folder.objects.get(pk=file_parent_id)
        
        new_file = File(file_path=file, owner=request.user, file_parent=file_parent)
        
        new_file.file_name = file.name
        new_file.file_size = file.size
        new_file.file_timestamp = timezone.now()
        
        new_file.save()

        return redirect('drive')
    else:
        return redirect('drive')
    
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        # Create folder logic here
        return redirect('folder_view')

@login_required
def drive_view(request):


    folder_list = Folder.objects.filter(folder_parent__isnull=True)
    file_list = File.objects.filter(file_parent__isnull=True)
    folder_number = Folder.objects.count()
    file_number = File.objects.count()

    used_quota_bytes = File.objects.all().aggregate(total_size=models.Sum('file_size'))['total_size'] or 0
    used_quota_mbs = round(used_quota_bytes / (1024 * 1024), 2)

    context = {
        'folder_list': folder_list,
        'file_list': file_list,
        "folder_number": folder_number,
        "file_number": file_number,
        'used_quota': f"{used_quota_mbs} MB",
    }

    return render(request, 'drive.html', context=context)

@login_required
def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    subfolders = Folder.objects.filter(folder_parent=folder)
    files_in_folder = File.objects.filter(file_parent=folder)

    used_quota_bytes = File.objects.all().aggregate(total_size=models.Sum('file_size'))['total_size'] or 0
    used_quota_mbs = round(used_quota_bytes / (1024 * 1024), 2)

    context = {
        'folder': folder,
        'subfolders': subfolders,
        'files': files_in_folder,
        'used_quota': f"{used_quota_mbs} MB",
    }

    return render(request, 'folder_detail.html', context)

# FILE MANAGEMENT VIEWS

@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, file_id=file_id)
    response = FileResponse(file.file_path.open('rb'), as_attachment=True, filename=file.file_name)

    return response

login_required
def view_file(request, file_id):
    file = get_object_or_404(File, file_id=file_id)
    response = FileResponse(file.file_path.open('rb'), filename=file.file_name)

    return response

@login_required
@require_POST
def delete_file(request, file_id):
    file = get_object_or_404(File, file_id=file_id)
    file.file_path.delete()
    file.delete()

    return redirect('drive')

@login_required
@require_POST
def rename_file(request, file_id):
    file = get_object_or_404(File, file_id=file_id)
    new_name = request.POST.get('new_name')

    _, ext = os.path.splitext(file.file_name)
    
    file.file_name = new_name + ext
    file.save()
    
    return redirect('drive')

# FOLDER MANAGEMENT VIEWS

@login_required
def download_folder(request, folder_id):
    folder = get_object_or_404(Folder, folder_id=folder_id)
    files = File.objects.filter(file_parent=folder)

    response = HttpResponse(content_type='application/zip')
    zip_file = zipfile.ZipFile(response, 'w')

    for file in files:
        file_path = file.file_path.path
        zip_file.write(file_path, arcname=file.file_name)

    zip_file.close()
    response['Content-Disposition'] = f'attachment; filename={folder.folder_name}.zip'
    return response

@login_required
@require_POST
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, folder_id=folder_id)
    folder.delete()

    return redirect('drive')

@login_required
@require_POST
def rename_folder(request, folder_id):
    folder = get_object_or_404(Folder, folder_id=folder_id)
    new_name = request.POST.get('new_name')
    
    folder.folder_name = new_name
    folder.save()
    
    return redirect('drive')

