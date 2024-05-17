from django import forms
from .models import Employee
from .models import *

class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'address', 'id_proof', 'resume']


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'requirements', 'qualifications', 'close_date']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee_id', 'leave_type', 'start_date', 'end_date', 'reason','status']