from django.db import models
from django.db.models import Avg

class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.department_name


    def calculate_score(self):
        total_tasks = self.tasklist_set.count()
        if total_tasks == 0:
            self.score = 0
            self.save()
            return

        score_sum = 0
        for task in self.tasklist_set.all():
            if task.status == 'PENDING':
                score_sum += 0
            elif task.status == 'STARTED':
                score_sum += 33.3
            elif task.status == 'IN_PROGRESS':
                score_sum += 66.6
            elif task.status == 'COMPLETED':
                score_sum += 100

        self.score = int(score_sum / total_tasks)
        self.save()
    @staticmethod
    def aggregate_score():
        return round(Department.objects.aggregate(average_score=Avg('score'))['average_score'],2) or 0

class TaskList(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    task = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    target_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')

    def __str__(self):
        return self.task

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.department.calculate_score()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.department.calculate_score()