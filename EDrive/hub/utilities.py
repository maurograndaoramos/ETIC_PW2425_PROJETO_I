from django.shortcuts import redirect
from django.db.models import Sum
from drive.models import File
from web.models import UserProfile

def calculate_used_quota(user):

    total_size = sum(file.file_size for file in File.objects.filter(owner=user))
    return round(total_size / (1024 * 1024), 2)

def calculate_available_quota(user):
    user_profile = UserProfile.objects.get(user=user)
    available_quota = user_profile.quota - calculate_used_quota(user)

    return round(available_quota, 2)

def has_enough_quota(user, file_size):
    available_quota_mb = calculate_available_quota(user)
    file_size_mb = file_size / (1024 * 1024)
    return available_quota_mb >= file_size_mb


def staff_redirect_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated and request.user.is_staff and not request.path.startswith('/admin/'):
            return redirect('admin:index')
        response = get_response(request)
        return response

    return middleware