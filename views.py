from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, AddUserForm, AddDepartmentForm, AddTasksForm, UpdateProfileForm
from django.contrib import messages
from .models import UserProfile, Department, Task
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model




def WelcomeView(request):

    return render(request, 'home.html')


def RegisterView(request):
    user = None

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
             user_manager = UserProfile.objects
             user = user_manager.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role=form.cleaned_data['role'],
            )
             if user:
                send_signup_email(user)
                return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Adding users/staff - done by admin
@login_required(login_url='/login/')
def AddUserView(request):
    User = get_user_model()
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            send_signup_email(user, password)

            return redirect('add_user')  
    else:
        form = AddUserForm()

    return render(request, 'add_user.html', {'form': form})


def send_signup_email(user, password):
    try:
        subject = 'Welcome to GalaxyC'
        message = f"Below are your login credentials.\nUsername: {user.email}\nPassword: {password}\n"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

    except Exception as e:
        print(f"Email sending failed: {e}")



# Login Functionality
def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check the user's role and redirect accordingly
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'employee':
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def UpdateProfileView(request):
    user = request.user  
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')  
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, 'update_profile.html', {'form': form})

def LogoutView(request):
    logout(request)
    return redirect('home')

def DashboardView(request):
    
    return render(request, 'dashboard.html')

def AdminDashboardView(request):
    
    return render(request, 'admin_dashboard.html')

def StaffView(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
    else:
        users = None  
    
    return render(request, 'staff.html', {'users': users})

@login_required
def DepartmentsView(request):
    if request.method == 'POST':
        form = AddDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments')  
    else:
        form = AddDepartmentForm()
        departments = Department.objects.all()
    
    return render(request, 'departments.html', {'form': form, 'departments': departments})



def TasksView(request, user_id=None):
    if request.method == 'POST':
        form = AddTasksForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('staff_list') 
    else:
        initial_data = {'assigned_to': user_id} if user_id else {}
        form = AddTasksForm(initial=initial_data)
    tasks = Task.objects.all()
    return render(request, 'add_tasks.html', {'form': form, 'tasks': tasks})


# function for sending assign email
def send_assignment_email(assigned_user):
    print(assigned_user)
    try:
        subject = 'Hello GalaxyC'
        message = f"You have been assigned a task."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [assigned_user.email]

        send_mail(subject, message, from_email, recipient_list)
        print(assigned_user)
    except Exception as e:
        print(f"Email sending failed: {e}")


def task_tracking_view(request):
    all_tasks = Task.objects.all()

    completed_tasks = all_tasks.filter(status='done')  
    uncompleted_tasks = all_tasks.exclude(status='done')  
    all = all_tasks

    total_tasks = all_tasks.count()
    if total_tasks > 0:
        percentage_done = (completed_tasks.count() / total_tasks) * 100
    else:
        percentage_done = 0

    context = {
        'done': completed_tasks,
        'pending': uncompleted_tasks,
        'incomplete': percentage_done,
        'my_tasks' : all,
    }

    return render(request, 'task_tracking.html', context)



def MyTasksView(request):
    all_tasks = Task.objects.filter(assigned_to=request.user)

    completed_tasks = all_tasks.filter(status='done')  
    uncompleted_tasks = all_tasks.exclude(status='done')

    total_tasks = all_tasks.count()
    if total_tasks > 0:
        percentage_done = (completed_tasks.count() / total_tasks) * 100
    else:
        percentage_done = 0

    context = {
        'done': completed_tasks,
        'pending': uncompleted_tasks,
        'incomplete': percentage_done,
        'my_tasks': all_tasks  
    }
    
    return render(request, 'task_tracking.html', context)



def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = 'done'
    task.save()

    if request.user.groups.filter(name='Admins').exists():
        return redirect('view_tasks')  
    else:
        return redirect('my_tasks')
    # return redirect('my_tasks')
