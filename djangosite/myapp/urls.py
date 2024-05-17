from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.userreg, name='userreg'),
    path('insertuser/', views.insertuser, name='insertuser'),
    path('approval_pending/', views.approval_pending, name='approval_pending'),
    path('request_leave/', views.request_leave, name='request_leave'),
    path('approve_leave/', views.approve_leave, name='approve_leave'),
    path('reject_leave/', views.reject_leave, name='reject_leave'),
    path('job_post/', views.job_post, name='job_post'),
    path('publish_job_post/', views.publish_job_post, name='publish_job_post'),
    path('job_posts/', views.job_post_list, name='job_post_list'),  # Correct URL pattern
    path('delete_job_post/', views.delete_job_post, name='delete_job_post'),
    path('publish_job_post1/', views.publish_job_post1, name='publish_job_post1'),
    path('create_job_post/', views.create_job_post, name='create_job_post'),
    path('pending_to_publish/', views.pending_to_publish, name='pending_to_publish'),
    path('main/', views.main1, name='main'),
    path('login/', views.login, name='login'),
    path('login_to_submit/', views.login_to_submit, name='login_to_submit'),
    path('hr_dashboard/<str:emp_id>/', views.hr_dashboard, name='hr_dashboard'),
    path('employee_dashboard/<str:emp_id>/', views.employee_dashboard, name='employee_dashboard'),
    path('pending_leave_requests/', views.pending_leave_requests_page, name='pending_leave_requests'),
    path('leave_balance/', views.leave_balance, name='leave_balance'),
    path('error_page/', views.error_page, name='error_page'),
    path('generate_payroll/', views.generate_payroll, name='generate_payroll'),
    path('employee_payslip/', views.employee_payslip, name='employee_payslip'),
]
