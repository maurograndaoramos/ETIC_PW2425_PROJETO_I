from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import upload_file, create_folder

urlpatterns = [
    path('', login_required(views.drive_view), name='drive'),
    path('folder/<int:folder_id>/', login_required(views.folder_view), name='folder'),
    path('upload/', upload_file, name='upload_file'),
    path('create_folder/', create_folder, name='create_folder'),

    # File management URLs
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
    path('view-file/<int:file_id>/', views.view_file, name='view_file'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('rename-file/<int:file_id>/', views.rename_file, name='rename_file'),
    
    path('move-file/<int:file_id>/', views.move_file, name='move_file'),


    # Folder management URLs
    path('download-folder/<int:folder_id>/', views.download_folder, name='download_folder'),
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('rename-folder/<int:folder_id>/', views.rename_folder, name='rename_folder'),
    path('move-folder/<int:folder_id>/', views.move_folder, name='move_folder'),
]