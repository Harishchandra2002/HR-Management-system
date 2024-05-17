from django.contrib import admin
from .models import Payroll

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'attendance', 'leaves', 'basic_salary', 'deductions', 'pay_date')
