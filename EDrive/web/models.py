from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    TIER_CHOICES = [
        ('Free', 'Free'),
        ('Premium', 'Premium'),
        ('Premium_Plus', 'Premium Plus'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='Free')

    @property
    def quota(self):
        if self.tier == 'Free':
            return 50
        elif self.tier == 'Premium':
            return 100
        elif self.tier == 'Premium_Plus':
            return 500
        return 0

    def __str__(self):
        return self.user.username
