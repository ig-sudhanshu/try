from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    # Add custom fields if needed
    # ...
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_groups",  # Add related_name here
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Add related_name here
        related_query_name="customuser",
    )
    class Meta:
        # Define related_name attributes to avoid clashes
        permissions = []  # You can define custom permissions here if needed
        
    def __str__(self):
        return self.username


# Create your models here.
