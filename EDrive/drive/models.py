from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import os
import hashlib

# Create your models here.



class File(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(default=0)
    file_path = models.FileField(upload_to="drive/uploads/")
    file_parent = models.ForeignKey("Folder", on_delete=models.CASCADE, null=True, default=0, blank=True)
    file_timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=64, editable=False, unique=True)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ["file_name"]
        indexes = [
            models.Index(fields=["file_name"]),
            models.Index(fields=["hash"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return "{} ({} MB)".format(self.file_name, round(self.file_size / 1024 / 1024, 2))

    def get_full_path(self):
        return self.file_path.url

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.file_path:
                self.file_size = self.file_path.size
                self.file_name = self.file_path.name

            original_full_path = self.file_path.path

            original_name = os.path.basename(original_full_path)
            hash_input = f"{self.file_id}{self.file_timestamp}{self.file_name}"
            self.hash = hashlib.sha256(hash_input.encode()).hexdigest()
            file_extension = os.path.splitext(original_name)[1]
            new_filename = f"{self.hash}{file_extension}"

            self.file_path.name = new_filename

        super().save(*args, **kwargs)

    
class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=255)
    folder_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subfolders', help_text="Parent Folder")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"
        ordering = ["folder_name"]
        indexes = [
            models.Index(fields=["folder_name"]),
            models.Index(fields=["owner"]),
        ]

    def get_absolute_url(self):
        return reverse('folder', args=[str(self.folder_id)])
    
    def __str__(self):
        return self.folder_name
