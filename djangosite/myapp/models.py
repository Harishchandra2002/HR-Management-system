from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    id_proof = models.ImageField(upload_to='id_proofs/')
    resume = models.FileField(upload_to='resumes/')
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = "employee"


class Employee_Data(models.Model):
    emp_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    employee_email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    leave_balance = models.IntegerField(default=10)

    class Meta:
        db_table = "employees_data"


class JobPost(models.Model):
    PENDING = 'Pending'
    PUBLISHED = 'Published'
    CLOSED = 'Closed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PUBLISHED, 'Published'),
        (CLOSED, 'Closed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    qualifications = models.TextField()
    close_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        db_table = "job_post"
