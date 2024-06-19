import os
import zipfile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from drive.models import File, Folder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from hub.utilities import calculate_used_quota


@login_required
def drive_view(request):
    current_user = request.user

    folder_list = Folder.objects.filter(owner=current_user, folder_parent__isnull=True)
    file_list = File.objects.filter(owner=current_user, file_parent__isnull=True)
    folder_number = Folder.objects.filter(owner=current_user).count()
    file_number = File.objects.filter(owner=current_user).count()

    used_quota_mbs = calculate_used_quota(current_user)


    context = {
        'folder_list': folder_list,
        'file_list': file_list,
        "folder_number": folder_number,
        "file_number": file_number,
        'used_quota': f"{used_quota_mbs} MB",
    }

    if request.user.is_staff:
        return redirect('admin:index')
    else:
        return render(request, 'drive.html', context=context)
    

@login_required
def folder_view(request, hash):
    current_user = request.user

    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    subfolders = Folder.objects.filter(folder_parent=folder, owner=current_user).order_by('folder_name')
    files_in_folder = File.objects.filter(file_parent=folder, owner=current_user)

    used_quota_mbs = calculate_used_quota(current_user)

    context = {
        'folder': folder,
        'subfolders': subfolders,
        'files': files_in_folder,
        'used_quota': f"{used_quota_mbs} MB",
    }

    if request.user.is_staff:
        return redirect('admin:index')
    else:
        return render(request, 'folder_detail.html', context)
    

# FILE MANAGEMENT VIEWS

@login_required
def download_file(request, hash):
    current_user = request.user
    file = get_object_or_404(File, hash=hash, owner=current_user)
    response = FileResponse(file.file_path.open('rb'), as_attachment=True, filename=file.file_name)
    return response

@login_required
def view_file(request, hash):
    current_user = request.user
    file = get_object_or_404(File, hash=hash, owner=current_user)
    response = FileResponse(file.file_path.open('rb'), filename=file.file_name)
    return response

@login_required
@require_POST
def delete_file(request, hash):
    current_user = request.user
    file = get_object_or_404(File, hash=hash, owner=current_user)
    file.file_path.delete()
    file.delete()
    if file.file_parent:
        return redirect('folder', hash=file.file_parent.hash)
    else: 
        return redirect('drive')

@login_required
@require_POST
def rename_file(request, hash):
    current_user = request.user
    file = get_object_or_404(File, hash=hash, owner=current_user)
    new_name = request.POST.get('new_name')
    _, ext = os.path.splitext(file.file_name)
    file.file_name = new_name + ext
    file.save()
    if file.file_parent:
        return redirect('folder', hash=file.file_parent.hash)
    else: 
        return redirect('drive')

@login_required
@require_POST
def move_file(request, hash):
    current_user = request.user
    file = get_object_or_404(File, hash=hash, owner=current_user)
    new_folder_id = request.POST.get('folder_id')
    new_folder = Folder.objects.get(pk=new_folder_id)
    file.file_parent = new_folder
    file.save()
    if file.file_parent:
        return redirect('folder', hash=file.file_parent.hash)
    else: 
        return redirect('drive')


# FOLDER MANAGEMENT VIEWS

@login_required
def download_folder(request, hash):
    current_user = request.user
    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    files = File.objects.filter(file_parent=folder, owner=current_user)
    
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
def delete_folder(request, hash):
    current_user = request.user
    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    folder.delete()
    if folder.folder_parent:
        return redirect('folder', hash=folder.folder_parent.hash)
    else: 
        return redirect('drive')

@login_required
@require_POST
def rename_folder(request, hash):
    current_user = request.user
    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    new_name = request.POST.get('new_name')
    folder.folder_name = new_name
    folder.save()
    if folder.folder_parent:
        return redirect('folder', hash=folder.folder_parent.hash)
    else: 
        return redirect('drive')

@login_required
@require_POST
def move_folder(request, folder_id):
    current_user = request.user
    folder = get_object_or_404(Folder, pk=folder_id, owner=current_user)  # Use pk for clarity
    new_folder_id = request.POST.get('folder_id')
    new_folder = Folder.objects.get(pk=new_folder_id)
    
    folder.folder_parent = new_folder
    folder.save()
    return redirect('folder', folder_id=new_folder_id)


# FILE UPLOAD AND FOLDER CREATION VIEWS
@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_parent_hash = request.POST.get('folder_id', None)
        file_parent = None

        if file_parent_hash:
            file_parent = Folder.objects.get(hash=file_parent_hash)
        
        new_file = File(file_path=file, owner=request.user, file_parent=file_parent)
        new_file.file_name = file.name
        new_file.file_size = file.size
        new_file.file_timestamp = timezone.now()
        new_file.save()

        if file_parent:
            return redirect('folder', file_parent_hash)
        else:
            return redirect('drive')
    else:
        return redirect('drive')

@login_required
def upload_folder(request):
    if request.method == 'POST':
        folder_parent_hash = request.POST.get('folder_id', None)
        folder_parent = None

        if folder_parent_hash:
            folder_parent = Folder.objects.get(hash=folder_parent_hash)

        files = request.FILES.getlist('folder')
        for f in files:
            new_file = File(file_path=f, owner=request.user, file_parent=folder_parent)
            new_file.file_name = f.name
            new_file.file_size = f.size
            new_file.file_timestamp = timezone.now()
            new_file.save()

        if folder_parent:
            return redirect('folder', folder_hash=folder_parent_hash)
        else:
            return redirect('drive')
    else:
        return redirect('drive')

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        parent_folder_hash = request.POST.get('folder_id', None)
        folder_parent = None

        if parent_folder_hash:
            folder_parent = Folder.objects.get(hash=parent_folder_hash)

        new_folder = Folder(folder_name=folder_name, owner=request.user, folder_parent=folder_parent)
        new_folder.save()

        if folder_parent:
            return redirect('folder', parent_folder_hash)  
        else:
            return redirect('drive')
    else:
        return redirect('drive')