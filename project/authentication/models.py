from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class CustomUser(AbstractUser):
    User.objects.create_user(username='testuser', password='password123', is_staff=False)
    pass
