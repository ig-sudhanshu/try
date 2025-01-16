from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('department/<int:department_id>/', views.department_tasks, name='department_tasks'),
    # path('department/<int:department_id>/add_task/', views.add_task, name='add_task'),
    # path('task/update/<int:task_id>/', views.update_task, name='update_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('department/add/', views.add_department, name='add_department'),
    path('department/update/<int:department_id>/', views.update_department, name='update_department'),
    path('department/delete/<int:pk>/', views.DepartmentDelete.as_view(), name='delete_department'),
    # path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    # path('update_task_priority/<int:task_id>/', views.update_task_priority, name='update_task_priority'),
    # path('update_task_target_date/<int:task_id>/', views.update_task_target_date, name='update_task_target_date'),
]