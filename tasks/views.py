from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from .models import Department, TaskList
from .forms import TaskForm, DepartmentForm  # Import TaskForm
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import DeleteView
import json
from django.core.serializers.json import DjangoJSONEncoder

def dashboard(request):
    departments = Department.objects.all().order_by('-score')
    aggregate_score = Department.aggregate_score()
    context = {
        'departments': departments,
        'aggregate_score': aggregate_score,
    }
    return render(request, 'tasks/dashboard.html', context)

# def department_tasks(request, department_id):
#     department = get_object_or_404(Department, pk=department_id)
#     tasks = department.tasklist_set.all()
#     score = department.score

#     if request.method == 'POST':
#         if 'add_task' in request.POST:
#             # Handle adding a new task
#             form = TaskForm(request.POST)
#             if form.is_valid():
#                 task = form.save(commit=False)
#                 task.department = department  # Pre-populate department
#                 task.save()
#                 return redirect('department_tasks', department_id=department_id)
#         elif 'update_task' in request.POST:
#             # Handle updating an existing task
#             task_id = request.POST.get('task_id')
#             task = get_object_or_404(TaskList, pk=task_id)
            
#             # Update task fields from the form
#             task.task = request.POST.get('task')
#             task.target_date = parse_date(request.POST.get('target_date'))
#             task.status = request.POST.get('status')
#             task.remarks = request.POST.get('remarks')
#             task.priority = request.POST.get('priority')
            
#             task.save()
#             return redirect('department_tasks', department_id=department_id)

#     else:
#         form = TaskForm(initial={'department': department})

#     add_task_flag = request.GET.get('show_add_task_form')

#     status_choices = json.dumps(list(TaskList.STATUS_CHOICES), cls=DjangoJSONEncoder)
#     priority_choices = json.dumps(list(TaskList.PRIORITY_CHOICES), cls=DjangoJSONEncoder)


#     context = {
#         'department': department,
#         'tasks': tasks,
#         'score': score,
#         'form': form,
#         'show_add_task_form': add_task_flag , # Initially hide the form
#         'status_choices': status_choices,  # Pass serialized data to template
#         'priority_choices': priority_choices,
#     }
#     return render(request, 'tasks/department_tasks.html', context)




def department_tasks(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    tasks = department.tasklist_set.all()
    score = department.score

    if request.method == 'POST':
        if 'add_task' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.department = department
                task.save()
                return redirect('department_tasks', department_id=department_id)
        elif 'update_task' in request.POST:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(TaskList, pk=task_id)
            
            task.task = request.POST.get('task')
            task.target_date = parse_date(request.POST.get('target_date'))
            task.status = request.POST.get('status')
            task.remarks = request.POST.get('remarks')
            task.priority = request.POST.get('priority')
            
            task.save()

            # Calculate the updated score
            department.calculate_score()
            new_score = department.score

            # Return JSON response
            return JsonResponse({'success': True, 'new_score': new_score})

    else:
        form = TaskForm(initial={'department': department})

    add_task_flag = request.GET.get('show_add_task_form')
    status_choices = json.dumps(list(TaskList.STATUS_CHOICES), cls=DjangoJSONEncoder)
    priority_choices = json.dumps(list(TaskList.PRIORITY_CHOICES), cls=DjangoJSONEncoder)

    context = {
        'department': department,
        'tasks': tasks,
        'score': score,
        'form': form,
        'show_add_task_form': add_task_flag,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
    }
    return render(request, 'tasks/department_tasks.html', context)


def delete_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    department_id = task.department.id
    task.delete()
    return redirect('department_tasks', department_id=department_id)

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'tasks/add_department.html', {'form': form})

def update_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'tasks/update_department.html', {'form': form})

class DepartmentDelete(DeleteView):
    model = Department
    success_url = reverse_lazy('dashboard')
    template_name = 'tasks/delete_department.html'