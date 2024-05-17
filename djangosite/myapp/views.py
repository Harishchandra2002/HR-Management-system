from datetime import datetime
import csv
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import EmployeeRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .forms import *
from django.core.mail import send_mail, EmailMessage
from .models import *
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse



# Create your views here.
def userreg(request):
    return render(request, "myapp/userreg.html", {})

def employee_page(request, emp_id):
    return render(request, 'myapp/employee_page.html')


def delete_job_post(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('job_post_id')
        print(f"Received job_post_id: {job_post_id}")  # This will print the job_post_id
        try:
            job_post = JobPost.objects.get(id=job_post_id)
            job_post.delete()
            messages.success(request, 'Job post deleted successfully.')
            return redirect('job_post_list')  # Redirect to the job post list page after deletion
        except JobPost.DoesNotExist:
            return render(request, 'myapp/error.html', {'message': 'Job post not found.'})
    else:
        return redirect('error_page')


def main1(request):
    return render(request, "myapp/main.html")

def login(request):
    return render(request, "myapp/login.html")

def hr_dashboard(request, emp_id):
    return render(request, "myapp/hr_dashboard.html")

def employee_dashboard(request, emp_id):
    return render(request, "myapp/employee_dashboard.html")


def generate_payroll(request):
    # Handle form submission for generating payroll
    return render(request, 'myapp/payrole.html')

def employee_payslip(request):
    # Retrieve and pass payroll data to the template
    return render(request, 'myapp/payslip.html')


def login_to_submit(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employeeId')
        password = request.POST.get('password')

        try:
            employee = Employee_Data.objects.get(emp_id=employee_id, password=password)
            # request.session['employee_id'] = employee_id
            # request.session['employee_name'] = employee.employee_name

            if employee_id.startswith('6'):
                # Redirect to HR page
                return redirect('hr_dashboard', emp_id=employee_id)
            elif employee_id.startswith('5'):
                # Redirect to employee page
                return redirect('employee_page', emp_id=employee_id)
            else:
                # Invalid employee ID format
                messages.error(request, 'Invalid employee ID format.')
                return redirect('login')
        except Employee_Data.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, "myapp/login.html")

def pending_to_publish(request):
    job_posts = JobPost.objects.filter(status=JobPost.PENDING)
    return render(request, 'myapp/pending_to_publish.html', {'job_posts': job_posts})



def error_page(request):
    return render(request, 'myapp/error.html')
def job_post(request):
    return render(request, "myapp/job_post.html")

def create_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.posted_by = request.user
            job_post.posted_on = timezone.now()
            job_post.save()
            messages.success(request, 'Job post created successfully!')
            return redirect('job_post_list')  # Correct redirection to job post list
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = JobPostForm()
    return render(request, 'myapp/create_job_post.html', {
        'form': form,
        'user': request.user,
        'current_date': timezone.now().strftime('%Y-%m-%d')
    })

def job_post_list(request):
    job_posts = JobPost.objects.filter(status=JobPost.PENDING)
    return render(request, 'myapp/pending to publish.html', {'job_posts': job_posts})

def publish_job_post(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('job_post_id')
        try:
            job_post = JobPost.objects.get(id=job_post_id)
            job_post.status = JobPost.PUBLISHED
            job_post.save()
            messages.success(request, 'Job post published successfully!')
        except JobPost.DoesNotExist:
            messages.error(request, 'Job post does not exist.')
    else:
        messages.error(request, 'Invalid request method.')

    return redirect('job_post_list')
def publish_job_post1(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('job_post_id')
        print(f"Received job_post_id: {job_post_id}")  # This will print the job_post_id
        try:
            job_post = JobPost.objects.get(id=job_post_id)
            job_post.status = JobPost.PUBLISHED
            job_post.save()
            messages.success(request, 'Job post published successfully!')
        except JobPost.DoesNotExist:
            messages.error(request, 'Job post does not exist.')
        return redirect('job_post_list')  # Redirect to the job post list page
    else:
        return redirect('error_page')


def index(request):
    return render(request, 'myapp/index.html')


def request_leave(request):
    if request.method == 'POST':
        # Handle form submission
        employee_id = request.POST.get('employee_id')
        leave_type = request.POST.get('leave_type')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        print(start_date_str)
        print(end_date_str)
        # Adjust the parsing format to '%Y-%m-%d'
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        num_days = (end_date - start_date).days
        # Convert date strings to YYYY-MM-DD format

        reason = request.POST.get('reason')


        # Fetch additional employee data from the database
        employee_data = Employee_Data.objects.filter(emp_id=employee_id).first()
        if employee_data:
            emp_name = employee_data.employee_name
            leave_balance = employee_data.leave_balance

            # Save the leave request data to the LeaveRequest table
            leave_request = LeaveRequest.objects.create(employee_id=employee_id, leave_type=leave_type,
                                                        start_date=start_date, end_date=end_date,
                                                        reason=reason)

            # Send email notification to HR
            send_leave_request_notification_to_hr({
                'employee_id': employee_id,
                'start_date': start_date,
                'end_date': end_date,
                'reason': reason,
                'leave_type': leave_type,
                'no_days': num_days,

            }, emp_name, leave_balance)

            # Optionally, you can redirect the user to a success page
            return redirect('leave_balance',employee_id=employee_id)
        else:
            return HttpResponseBadRequest("Employee data not found")

    return render(request, 'myapp/request_leave.html')


def approve_leave(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        leave_request_id = request.POST.get('leave_request_id')

        # Get all LeaveRequest objects with the given emp_id and leave_request_id
        leave_requests = LeaveRequest.objects.filter(employee_id=emp_id, id=leave_request_id)

        if leave_requests.exists():
            # Update status and send email notification for each leave request
            for leave_request in leave_requests:
                leave_request.status = 'approved'
                leave_request.save()
                send_leave_notification_to_employee(emp_id, approved=True)

            return redirect('pending_leave_requests')  # Redirect to leave balance page after approval
        else:
            # Handle case where leave request data does not exist
            return JsonResponse({'error': 'Leave request data does not exist'}, status=404)

    # Handle GET requests or other cases where the method is not POST
    return HttpResponseNotAllowed(['POST'])


def reject_leave(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        leave_request_id = request.POST.get('leave_request_id')
        leave_requests = LeaveRequest.objects.filter(employee_id=emp_id, id=leave_request_id)
        if leave_requests.exists():
            # Update status and send email notification for each leave request
            for leave_request in leave_requests:
                leave_request.status = 'rejected'
                leave_request.save()
                send_leave_notification_to_employee(emp_id, approved=False)

            return redirect('pending_leave_requests')  # Redirect to page displaying pending leave requests
        else:
            # Handle case where leave request data does not exist
            return JsonResponse({'error': 'Leave request data does not exist'}, status=404)

    # Handle GET requests or other cases where the method is not POST
    return HttpResponseNotAllowed(['POST'])

def send_leave_notification_to_employee(emp_id, approved):
    # Retrieve employee data
    employee_data = Employee_Data.objects.get(emp_id=emp_id)
    employee_email = employee_data.employee_email
    employee_name = employee_data.employee_name

    # Compose email subject and message based on approval status
    subject = 'Leave Request Update'
    if approved:
        message = f'Hello {employee_name},\n\nYour leave request has been approved.'
    else:
        message = f'Hello {employee_name},\n\nYour leave request has been rejected.'

    # Send email
    send_mail(
        subject,
        message,
        'harishchandravallabhu@gmail.com',  # Update with your email address
        [employee_email],
    )


def send_leave_request_notification_to_hr(data, emp_name, leave_balance):
    subject = 'Leave Request Notification'
    # Render HTML template with leave request details
    html_message = render_to_string('myapp/hr_notification.html', {
        'emp_id': data['employee_id'],
        'emp_name': emp_name,
        'leave_balance': leave_balance,
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'reason': data['reason'],
        'leave_type': data['leave_type'],
    })
    from_email = 'harishchandravallabhu@gmail.com'  # Update with your email
    to_email = 'vallabhuharish03@gmail.com'  # Update with HR's email

    # Send email with HTML content
    send_mail(
        subject,
        '',  # Blank message as we are using html_message parameter
        from_email,
        [to_email],
        html_message=html_message,  # Include HTML content
    )


from django.core.exceptions import ValidationError



def insertuser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        id_proof = request.FILES.get('id_proof')
        resume = request.FILES.get('resume')

        # Check if email already exists
        # if Employee.objects.filter(email=email).exists():
        #     return JsonResponse({'success': False, 'errors': 'Email already exists'}, status=400)

        # Create and save Employee object
        try:
            employee = Employee(name=name, email=email, address=address, id_proof=id_proof, resume=resume)
            employee.full_clean()  # Validate model fields
            employee.save()
        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': e.message_dict}, status=400)

        # Return the URL for the login page after successful registration
        return JsonResponse({'success': True, 'redirect_url': reverse('login')})
    else:
        return JsonResponse({'success': False, 'errors': 'Method not allowed'}, status=405)

def approval_pending(request):
    # Retrieve details from the latest Employee object
    latest_employee = Employee.objects.last()
    if latest_employee:
        name = latest_employee.name
        email = latest_employee.email
        address = latest_employee.address

        # Generate employee ID
        last_employee_data = Employee_Data.objects.last()
        if last_employee_data:
            emp_id = last_employee_data.emp_id + 1
        else:
            emp_id = 50001

        # Save employee data to the database
        password = email  # Assuming password is same as email
        leave_balance = 10
        employee_data = Employee_Data.objects.create(
            emp_id=emp_id,
            employee_name=name,
            employee_email=email,
            password=password,
            leave_balance=leave_balance
        )

        # Send email to the user with employee details
        subject = 'Registration Confirmation'
        message = f'Hello {name},\n\nThank you for your registration. Your details are as follows:\n\nEmployee ID: {emp_id}\nUser ID: {email}\nPassword: {password}\n\nWe will process your request shortly.\n\nRegards,\nHarish Vallabhu'

        # Send confirmation email to the user
        email_to_user = EmailMessage(
            subject,
            message,
            to=[email],
        )
        email_to_user.send()

        # Compose email content for admin
        admin_subject = 'Pending Registration Approval'
        admin_message = f'Hello Harish,\n\nThis is to notify you about a pending registration approval for:\n\nName: {name}\nEmail: {email}\nAddress: {address}\n\nEmployee ID: {emp_id}\n\nPlease take necessary action.\n\nRegards,\nHarish Vallabhu'

        # Send email to admin
        send_mail(
            admin_subject,
            admin_message,
            'harishchandravallabhu@gmail.com',
            ['vallabhuharish03@gmail.com'],
        )

        # Render the approval_pending.html template
        return render(request, 'myapp/approval_pending.html', {})
    else:
        # Handle case when there are no Employee objects in the database
        return JsonResponse({'error': 'No employee data found'}, status=404)


def pending_leave_requests_page(request):
    # Retrieve pending leave requests from the database
    pending_leave_requests = LeaveRequest.objects.filter(status='pending')

    # Pass the pending leave requests data to the template
    return render(request, 'myapp/leave_request_page_to_hr.html', {'pending_leave_requests': pending_leave_requests})


def leave_balance(request):
    # Retrieve the employee_id from the request's query parameters
    employee_id = request.GET.get('employee_id', None)

    if employee_id is not None:
        # Retrieve leave balance history for the given employee ID
        leave_balance_history = LeaveRequest.objects.filter(employee_id=employee_id)
        # Pass the leave balance history and employee ID to the template
        return render(request, 'myapp/leave_balance.html',
                      {'leave_balance_history': leave_balance_history, 'employee_id': employee_id})
    else:
        # Handle case when employee_id is not provided
        return render(request, 'myapp/employee_id_missing.html')



def approve_payroll(request):
    if request.method == 'POST':
        # Extract the form data
        employee_id = request.POST.get('employee_id')
        attendance_str = request.POST.get('attendance')
        leaves_str = request.POST.get('leaves')
        deductions_str = request.POST.get('deductions')

        # Check if input values are not empty
        if attendance_str and leaves_str and deductions_str:
            try:
                # Convert input values to integers or floats
                attendance = int(attendance_str)
                leaves = int(leaves_str)
                deductions = float(deductions_str)

                # Add logic to calculate basic_salary based on attendance, leaves, etc.
                basic_salary = calculate_basic_salary(attendance, leaves)
                pay_date = timezone.now().date()  # Assuming the pay date is today

                # Get the employee's email address
                employee = Employee_Data.objects.get(emp_id=employee_id)
                employee_email = employee.employee_email

                # Send payroll approval notification
                send_payroll_approval_notification(employee_email)

                # Save payroll information to the database
                payroll = Payroll(
                    employee=employee,
                    attendance=attendance,
                    leaves=leaves,
                    basic_salary=basic_salary,
                    deductions=deductions,
                    pay_date=pay_date
                )
                payroll.save()

                # Redirect to the generate payroll page
                return redirect(reverse('generate_payroll'))
            except ValueError:
                return render(request, 'myapp/error.html', {'message': 'Invalid input values'})
            except Employee_Data.DoesNotExist:
                return render(request, 'myapp/error.html', {'message': 'Employee not found'})
        else:
            return render(request, 'myapp/error.html', {'message': 'Input fields cannot be empty'})
    else:
        return render(request, 'myapp/error.html', {'message': 'Invalid request method'})
def calculate_basic_salary(attendance, leaves):
    # Assuming the basic salary is $100 per day
    daily_salary = 1000
    total_days = 30  # Assuming a month has 30 days

    # Calculate the number of worked days
    worked_days = total_days - leaves

    # Calculate the basic salary based on attendance
    basic_salary = daily_salary * attendance

    return basic_salary
def send_payroll_approval_notification(employee_email):
    subject = 'Your Payroll Has Been Approved'
    message = 'Dear Employee,\n\nYour payroll has been approved. You can now view and download your payslip.'
    from_email = settings.EMAIL_HOST_USER
    to_email = [employee_email]

    try:
        send_mail(subject, message, from_email, to_email)
        return True
    except Exception as e:
        # Handle any exceptions that may occur during the email sending process
        print(f"Error sending email notification: {e}")
        return False

@login_required
def view_payslip(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You are not logged in.')
        return redirect('login')

    try:
        employee = Employee_Data.objects.get(emp_id=employee_id)
        payrolls = Payroll.objects.filter(employee=employee)
        return render(request, 'myapp/payslip.html', {
            'payrolls': payrolls,
            'employee_name': employee.employee_name
        })
    except Employee_Data.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('login')



def pay_login(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employeeId')
        password = request.POST.get('password')

        try:
            employee = Employee_Data.objects.get(emp_id=employee_id, password=password)
            # If employee found with provided ID and password
            # Proceed to fetch payroll and render payslip
            payrolls = Payroll.objects.filter(employee=employee)

            return render(request, 'myapp/emp_payslip.html', {
                'employee': employee,
                'payrolls': payrolls
            })
        except Employee_Data.DoesNotExist:
            # If employee with provided ID and password does not exist
            # Redirect back to login page with error message
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'myapp/login.html')
    else:
        # If not a POST request, render the login page
        return render(request, 'login.html')



def download_payslip(request):
    # Fetch payslip data for all employees (you need to implement this logic)
    all_payrolls = Payroll.objects.all()  # Assuming Payroll is your model

    # Create a CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payslip_data.csv"'

    # Write payslip data to CSV
    writer = csv.writer(response)
    writer.writerow(['Employee Name', 'Pay Date', 'Attendance', 'Leaves', 'Basic Salary', 'Deductions', 'Net Salary'])
    for payroll in all_payrolls:
        writer.writerow([
            payroll.employee.employee_name,
            payroll.pay_date,
            payroll.attendance,
            payroll.leaves,
            payroll.basic_salary,
            payroll.deductions,
            payroll.net_salary
        ])

    return response

def careers(request):
    # Retrieve published job posts
    published_jobs = JobPost.objects.filter(status=JobPost.PUBLISHED)
    return render(request, 'myapp/careers.html', {'published_jobs': published_jobs})


def job_application_form(request):
    return render(request, 'myapp/application.html')


def submit_application(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phn = request.POST.get('phn')
        degree = request.POST.get('degree')
        resume = request.FILES.get('resume')

        # Create a new JobApplicants object and save it to the database
        JobApplicants.objects.create(
            name=name,
            email=email,
            phn=phn,
            degree=degree,
            resume=resume
        )

        # Redirect to a success page or any other page
        return redirect('careers')  # Replace 'success_page' with the name of your success page URL

    # If the request method is not POST, render the form template
    return render(request, 'job_application_form.html')

def job_applications(request):
    applications = JobApplicants.objects.all()
    return render(request, 'myapp/job_application.html', {'applications': applications})