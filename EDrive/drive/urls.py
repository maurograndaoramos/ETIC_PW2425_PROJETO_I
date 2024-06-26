from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.drive_view), name='drive'),
    path('folder/<str:hash>/', login_required(views.folder_view), name='folder'),
    path('search/', views.search_view, name='search'),

    path('upload_file/', views.upload_file, name='upload_file'),
    path('upload_folder/', views.upload_folder, name='upload_folder'),

    path('create_folder/', views.create_folder, name='create_folder'),

    # File management URLs using hashes
    path('download-file/<str:hash>/', views.download_file, name='download_file'),
    path('view-file/<str:hash>/', views.view_file, name='view_file'),
    path('delete-file/<str:hash>/', views.delete_file, name='delete_file'),
    path('rename-file/<str:hash>/', views.rename_file, name='rename_file'),

    path('move-file/<str:hash>/', views.move_file, name='move_file'),

    # Folder management URLs using hashes
    path('download-folder/<str:hash>/', views.download_folder, name='download_folder'),
    path('delete-folder/<str:hash>/', views.delete_folder, name='delete_folder'),
    path('rename-folder/<str:hash>/', views.rename_folder, name='rename_folder'),

    path('move-folder/<str:hash>/', views.move_folder, name='move_folder'),
]