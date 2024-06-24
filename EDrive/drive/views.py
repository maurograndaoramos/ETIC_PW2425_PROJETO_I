import os
import zipfile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse, Http404
from drive.models import File, Folder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from hub.utilities import calculate_used_quota, calculate_available_quota, has_enough_quota
import shutil
from django.conf import settings


@login_required
def drive_view(request):
    current_user = request.user

    folder_list = Folder.objects.filter(owner=current_user, folder_parent__isnull=True)
    subfolder_list = Folder.objects.filter(owner=current_user, folder_parent=True)
    file_list = File.objects.filter(owner=current_user, file_parent__isnull=True)
    folder_number = Folder.objects.filter(owner=current_user).count()
    file_number = File.objects.filter(owner=current_user).count()

    used_quota_mbs = calculate_used_quota(current_user)
    user_quota = current_user.userprofile.quota
    user_quota_left = calculate_available_quota(current_user)
    quota_used_percentage = int(round((used_quota_mbs / user_quota) * 100, 0))

    context = {
        'folder_list': folder_list,
        'subfolder_list': subfolder_list,
        'file_list': file_list,
        "folder_number": folder_number,
        "file_number": file_number,
        'used_quota': f"{used_quota_mbs}",
        'user_quota': f"{user_quota}",
        'user_quota_left': f"{user_quota_left}",
        'quota_used_percentage': f"{quota_used_percentage}",
    }

    return render(request, 'drive.html', context=context)
    

@login_required
def folder_view(request, hash):
    current_user = request.user

    folder = get_object_or_404(Folder, hash=hash, owner=current_user)
    folder_list = Folder.objects.filter(folder_parent=folder, owner=current_user).order_by('folder_name')
    file_list = File.objects.filter(file_parent=folder, owner=current_user)

    used_quota_mbs = calculate_used_quota(current_user)
    user_quota = current_user.userprofile.quota
    user_quota_left = calculate_available_quota(current_user)
    quota_used_percentage = int(round((used_quota_mbs / user_quota) * 100, 0))

    context = {
        'folder': folder,
        'folder_list': folder_list,
        'file_list': file_list,
        'used_quota': f"{used_quota_mbs}",
        'user_quota': f"{user_quota}",
        'user_quota_left': f"{user_quota_left}",
        'quota_used_percentage': f"{quota_used_percentage}",
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
        messages.warning(request, "A file with that name already exists. Renamed to " + final_name + ".")
    else:
        messages.success(request, "File has been renamed to " + final_name + ".")

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
    messages.success(request, "File has been moved to " + new_folder + ".")
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
    else:
        messages.success(request, "Folder has been renamed to " + new_name + ".")

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
        
        original_name = folder.folder_name
        new_name = original_name
        counter = 1
        
        while Folder.objects.filter(folder_name=new_name, folder_parent=new_folder, owner=current_user).exists():
            counter += 1
            new_name = f"{original_name} ({counter})"
        
        if counter > 1:
            messages.error(request, "A folder with that name already exists in the destination. Renamed to " + new_name + ".")
            folder.folder_name = new_name
        else:
            messages.success(request, "Folder has been moved to " + new_folder.folder_name + ".")
        
        folder.folder_parent = new_folder
        folder.save()
    else:
        messages.error(request, "Invalid destination folder.")

    if folder.folder_parent:
        return redirect('folder', hash=folder.folder_parent.hash)
    else:
        return redirect('drive')
    
    # return redirect('folder', hash=folder.hash if folder.folder_parent else 'drive')


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
            messages.warning(request, "A file with that name already exists. Renamed to " + file_name + ".")
        else:
            messages.success(request, "File " + file_name + " has been uploaded.")

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
    
import logging

logger = logging.getLogger(__name__)

@login_required
def upload_folder(request):
    if request.method == 'POST':
        files = request.FILES.getlist('folder')
        file_paths = request.POST.getlist('file_paths')
        
        logger.debug(f"Number of files received: {len(files)}")
        logger.debug(f"Number of file paths received: {len(file_paths)}")
        
        for f, path in zip(files, file_paths):
            logger.debug(f"File name: {f.name}, Path: {path}")

    if request.method == 'POST':
        current_user = request.user
        folder_parent_hash = request.POST.get('folder_id')
        folder_parent = None

        if folder_parent_hash:
            try:
                folder_parent = get_object_or_404(Folder, hash=folder_parent_hash)
            except Http404:
                messages.error(request, "The specified parent folder does not exist.")
                return redirect('drive')

        files = request.FILES.getlist('folder')
        
        if not files:
            messages.error(request, "No files were selected for upload.")
            return redirect('folder', folder_parent.hash) if folder_parent else redirect('drive')

        total_size = sum(f.size for f in files)

        if not has_enough_quota(current_user, total_size):
            messages.error(request, "You do not have enough quota to upload these files.")
            return redirect('folder', folder_parent.hash) if folder_parent else redirect('drive')

        try:
            uploaded_files, created_folders, renamed_files = process_uploads(list(zip(files, file_paths)), current_user, folder_parent)
            logger.debug(f"Uploaded {uploaded_files} files, created {created_folders} folders, renamed {len(renamed_files)} files")
            
            for original_name, new_name in renamed_files:
                logger.debug(f"Renamed: {original_name} to {new_name}")
                messages.info(request, f"A file named '{original_name}' already exists. Renamed to '{new_name}'.")

            messages.success(request, f"Successfully uploaded {uploaded_files} files and created {created_folders} folders.")
        except Exception as e:
            logger.exception("Error during upload process")
            messages.error(request, f"An error occurred during the upload process: {str(e)}")

        return redirect('folder', folder_parent.hash) if folder_parent else redirect('drive')
    else:
        return redirect('drive')

def process_uploads(file_data, user, parent_folder):
    uploaded_files = 0
    created_folders = 0
    renamed_files = []
    folder_structure = {}
    temp_directories = set()
    logger.debug(f"Starting to process {len(file_data)} file entries")
    # First pass: Analyze file paths and create folder structure
    for file, path in file_data:
        path_parts = path.split('/')
        current_dict = folder_structure
        for part in path_parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
    # Second pass: Create folders
    def create_folders(structure, parent):
        nonlocal created_folders
        for folder_name, subfolders in structure.items():
            try:
                new_folder = Folder.objects.get(
                    folder_name=folder_name,
                    owner=user,
                    folder_parent=parent
                )
                logger.debug(f"Found existing folder: {folder_name}")
            except Folder.DoesNotExist:
                new_folder = Folder(
                    folder_name=folder_name,
                    owner=user,
                    folder_parent=parent,
                    created_at=timezone.now()
                )
                new_folder.save()
                created_folders += 1
                logger.debug(f"Created new folder: {folder_name}")
            create_folders(subfolders, new_folder)
    create_folders(folder_structure, parent_folder)
    logger.debug(f"Folder creation complete. Created {created_folders} folders.")
    # Third pass: Save files
    for file, path in file_data:
        path_parts = path.split('/')
        current_folder = parent_folder
        for part in path_parts[:-1]:
            current_folder = Folder.objects.get(folder_name=part, folder_parent=current_folder, owner=user)
        file_name = path_parts[-1]
        logger.debug(f"Saving file: {file_name} in folder: {current_folder.folder_name}")
        original_name, ext = os.path.splitext(file_name)
        counter = 1
        while File.objects.filter(file_name=file_name, file_parent=current_folder, owner=user).exists():
            counter += 1
            file_name = f"{original_name} ({counter}){ext}"
        if counter > 1:
            renamed_files.append((f"{original_name}{ext}", file_name))
            logger.debug(f"Renamed file to: {file_name}")
        # Debugging the path being constructed
        temp_dir = os.path.join(str(current_folder.folder_id))
        temp_directories.add(temp_dir)
        save_path = os.path.join(temp_dir, file_name)
        logger.debug(f"Save path: {save_path}")
        temp_path = default_storage.save(save_path, ContentFile(file.read()))
        new_file = File(
            file_path=temp_path,
            file_name=file_name,
            file_size=file.size,
            file_timestamp=timezone.now(),
            owner=user,
            file_parent=current_folder
        )
        new_file.save()
        uploaded_files += 1
        logger.debug(f"Saved file: {file_name}")
    # Remove temporary directories
    for temp_dir in temp_directories:
        full_temp_dir_path = os.path.join(settings.MEDIA_ROOT, temp_dir)
        if os.path.exists(full_temp_dir_path) and os.path.isdir(full_temp_dir_path):
            try:
                shutil.rmtree(full_temp_dir_path)
                logger.debug(f"Deleted temporary directory: {full_temp_dir_path}")
            except Exception as e:
                logger.error(f"Error deleting temporary directory {full_temp_dir_path}: {str(e)}")
    logger.debug(f"Upload complete. Uploaded {uploaded_files} files, created {created_folders} folders, renamed {len(renamed_files)} files.")
    return uploaded_files, created_folders, renamed_files

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
            messages.warning(request, "A folder with that name already exists. Renamed to " + folder_name + ".")
        else:
            messages.success(request, "Folder " + folder_name + " has been created.")

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