from django import forms
from .models import Employee
from .models import JobPost

class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'address', 'id_proof', 'resume']


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'requirements', 'qualifications', 'close_date']
