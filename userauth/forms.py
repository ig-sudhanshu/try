from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import Group

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')  # Add other fields as needed

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Assign user to a default group (e.g., EMPLOYEES)
            employees_group, created = Group.objects.get_or_create(name='EMPLOYEES')
            user.groups.add(employees_group)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser