import os
import zipfile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from drive.models import File, Folder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from hub.utilities import calculate_used_quota, has_enough_quota


@login_required
def drive_view(request):
    current_user = request.user

    folder_list = Folder.objects.filter(owner=current_user, folder_parent__isnull=True)
    file_list = File.objects.filter(owner=current_user, file_parent__isnull=True)
    folder_number = Folder.objects.filter(owner=current_user).count()
    file_number = File.objects.filter(owner=current_user).count()

    used_quota_mbs = calculate_used_quota(current_user)
    user_quota = current_user.userprofile.quota
    user_quota_left = user_quota - used_quota_mbs

    context = {
        'folder_list': folder_list,
        'file_list': file_list,
        "folder_number": folder_number,
        "file_number": file_number,
        'used_quota': f"{used_quota_mbs} MB",
        'user_quota': f"{user_quota} MB",
        'user_quota_left': f"{user_quota_left} MB",
    }

    return render(request, 'drive.html', context=context)
    

@login_required
def folder_view(request, hash):
    current_user = request.user

    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    subfolders = Folder.objects.filter(folder_parent=folder, owner=current_user).order_by('folder_name')
    files_in_folder = File.objects.filter(file_parent=folder, owner=current_user)

    used_quota_mbs = calculate_used_quota(current_user)
    user_quota = current_user.userprofile.quota

    context = {
        'folder': folder,
        'subfolders': subfolders,
        'files': files_in_folder,
        'used_quota': f"{used_quota_mbs} MB",
        'user_quota': f"{user_quota} MB",
    }

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

    counter = 1
    final_name = f"{new_name}{ext}"

    while File.objects.filter(file_name=final_name, file_parent=file.file_parent, owner=current_user).exists():
        counter += 1
        final_name = f"{new_name} ({counter}){ext}"

    if counter > 1:
        messages.error(request, "A file with that name already exists. Renamed to " + final_name + ".")

    file.file_name = final_name
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
    
    files_in_folder = File.objects.filter(file_parent=folder, owner=current_user)
    for file in files_in_folder:
        file.file_path.delete()
        file.delete()

    subfolders = Folder.objects.filter(folder_parent=folder, owner=current_user)
    for subfolder in subfolders:
        delete_subfolders(subfolder)

    folder.delete()
    
    if folder.folder_parent:
        return redirect('folder', hash=folder.folder_parent.hash)
    else: 
        return redirect('drive')

def delete_subfolders(folder):
    files_in_folder = File.objects.filter(file_parent=folder, owner=folder.owner)
    for file in files_in_folder:
        file.file_path.delete()
        file.delete()
    
    subfolders = Folder.objects.filter(folder_parent=folder, owner=folder.owner)
    for subfolder in subfolders:
        delete_subfolders(subfolder)
    
    folder.delete()

@login_required
@require_POST
def rename_folder(request, hash):
    current_user = request.user
    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    new_name = request.POST.get('new_name')

    original_name = new_name
    counter = 1

    while Folder.objects.filter(folder_name=new_name, owner=current_user, folder_parent=folder.folder_parent).exists():
        counter += 1
        new_name = f"{original_name} ({counter})"
    
    if counter > 1:
        messages.error(request, "A folder with that name already exists. Renamed to " + new_name + ".")

    folder.folder_name = new_name
    folder.save()
    
    if folder.folder_parent:
        return redirect('folder', hash=folder.folder_parent.hash)
    else:
        return redirect('drive')

@login_required
@require_POST
def move_folder(request, hash):
    current_user = request.user
    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    new_folder_hash = request.POST.get('destination_folder')

    if new_folder_hash and new_folder_hash != folder.hash:
        new_folder = get_object_or_404(Folder, hash=new_folder_hash, owner=current_user)
        folder.folder_parent = new_folder
        folder.save()
    else:
        messages.error(request, "Invalid destination folder.")
    
    if folder.folder_parent:
        return redirect('folder', hash=folder.folder_parent.hash)
    else:
        return redirect('drive')


# FILE UPLOAD AND FOLDER CREATION VIEWS
@login_required
def upload_file(request):
    current_user = request.user
    if request.method == 'POST':
        file = request.FILES['file']
        file_parent_hash = request.POST.get('folder_id', None)
        file_parent = None

        if file_parent_hash:
            file_parent = Folder.objects.get(hash=file_parent_hash)
            
        original_name, ext = os.path.splitext(file.name)
        file_name = file.name
        file_size = file.size

        if not has_enough_quota(current_user, file_size):
            messages.error(request, "You do not have enough quota to upload this file.")
            if file_parent:
                return redirect('folder', file_parent.hash)
            else:
                return redirect('drive')

        file_timestamp = timezone.now()
        counter = 1

        while File.objects.filter(file_name=file_name, file_parent=file_parent, owner=current_user).exists():
            counter += 1
            file_name = f"{original_name} ({counter}){ext}"

        if counter > 1:
            messages.error(request, "A file with that name already exists. Renamed to " + file_name + ".")

        temp_path = default_storage.save(file_name, ContentFile(file.read()))

        new_file = File(
            file_path=temp_path,
            file_name=file_name,
            file_size=file_size,
            file_timestamp=file_timestamp,
            owner=current_user,
            file_parent=file_parent
        )
        new_file.save() 

        if file_parent:
            return redirect('folder', file_parent.hash)
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
    current_user = request.user
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        parent_folder_hash = request.POST.get('folder_id', None)
        folder_parent = None

        if parent_folder_hash:
            folder_parent = Folder.objects.get(hash=parent_folder_hash)

        original_name = folder_name
        counter = 1

        while Folder.objects.filter(folder_name=folder_name, folder_parent=folder_parent, owner=current_user).exists():
                counter += 1
                folder_name = f"{original_name} ({counter})"
                
        if counter > 1:
            messages.error(request, "A file with that name already exists. Renamed to " + folder_name + ".")

        new_folder = Folder(
            folder_name=folder_name, 
            owner=current_user, 
            folder_parent=folder_parent
        )
        new_folder.save()

        if folder_parent:
            return redirect('folder', folder_parent.hash)  
        else:
            return redirect('drive')
    else:
        return redirect('drive')