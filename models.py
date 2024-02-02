from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, role='employee', department=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)

        # Check if a department is provided, otherwise create a default department
        if department is None:
            default_department, _ = Department.objects.get_or_create(name='HR Department')
            department = default_department

        user = self.model(email=email, role=role, department=department, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Assign user to appropriate group based on role
        if role == 'admin':
            admin_group, created = Group.objects.get_or_create(name='Admins')
            user.groups.add(admin_group)
        else:
            employee_group, created = Group.objects.get_or_create(name='Employees')
            user.groups.add(employee_group)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, role='admin', **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=100, default='employee')  # Default role is 'employee'
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.SET_NULL, null=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('incomplete', 'Incomplete'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name