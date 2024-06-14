from django.contrib import admin
from .models import File, Folder

# Register your models here.
@admin.register(File)
class ProductAdmin (admin.ModelAdmin):
    list_display = ('file_id', 'file_name', 'file_size', 'file_parent', 'hash', 'file_path', 'owner')
    list_filter = ('file_name', 'file_size', 'file_parent', 'owner')
    search_fields = ('file_name', 'file_size', 'file_parent', 'owner')
    ordering = ['file_name']

@admin.register(Folder)
class ProductAdmin (admin.ModelAdmin):
    list_display = ('folder_id', 'folder_name', 'folder_parent', 'owner')
    list_filter = ('folder_name', 'folder_parent', 'owner')
    search_fields = ('folder_name', 'folder_parent', 'owner')
    ordering = ['folder_name']
