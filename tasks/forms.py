from django import forms
from .models import TaskList, Department

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'department', 'status', 'target_date', 'remarks', 'priority']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']