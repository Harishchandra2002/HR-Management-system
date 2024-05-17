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
        fields = ['employee_id', 'leave_type', 'start_date', 'end_date', 'reason', 'status']


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee_id', 'leave_type', 'start_date', 'end_date', 'reason','status']

# performance_management/forms.py
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['description', 'deadline']

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['rating', 'feedback']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplicants
        fields = ['name', 'email', 'phn', 'degree', 'resume']

class DevelopmentPlanForm(forms.ModelForm):
    class Meta:
        model = DevelopmentPlan
        fields = ['program_name', 'description']
