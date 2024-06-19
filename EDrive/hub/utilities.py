from django.db.models import Sum
from drive.models import File

# Function to calculate the used quota of a user
def calculate_used_quota(user):
    total_size = File.objects.filter(owner=user).aggregate(total_size=Sum('file_size'))['total_size'] or 0
    total_size_mb = round(total_size / (1024 * 1024), 2)
    return total_size_mb

# Function to calculate the available quota of a user
def calculate_available_quota(user):
    available_quota = user.quota - calculate_used_quota(user)
    return available_quota

# Function to check if a user has enough quota to upload a file

def has_enough_quota(user, file_size):
    available_quota = calculate_available_quota(user)
    return available_quota >= file_size

# Function to check if a user has permission to access a file or folder

def has_permission(user, file):
    return user == file.owner
