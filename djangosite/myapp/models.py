from django.db import models
from django.contrib.auth.models import User

class JobApplicants(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phn = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)  # Assuming CharField for degree
    resume = models.FileField(upload_to='resumes/')

    class Meta:
        db_table = "JobApplicants"

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


class LeaveRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    employee_id = models.IntegerField()
    leave_type = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100, default='2024-05-23')  # Example default value
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        db_table = "LeaveRequest"


class Payroll(models.Model):
    # Your other fields
    employee = models.ForeignKey(Employee_Data, on_delete=models.CASCADE)
    pay_date = models.DateField()
    attendance = models.IntegerField()
    leaves = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def net_salary(self):
        # Calculate net salary based on basic_salary and deductions
        return self.basic_salary - self.deductions
    class Meta:
        db_table = "payroll"

# performance_management/models.py
from django.db import models

class Goal(models.Model):
    description = models.TextField()
    deadline = models.DateField()
    achieved = models.BooleanField(default=False)

class PerformanceReview(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()

class DevelopmentPlan(models.Model):
    program_name = models.CharField(max_length=100)
    description = models.TextField()

