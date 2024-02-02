from django import forms
from .models import UserProfile, Department, Task


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'] = forms.CharField(initial='admin', widget=forms.HiddenInput())


class AddUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()
        self.fields['role'] = forms.CharField(initial='employee', widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'role', 'department']

    # class Meta:
    #     model = UserProfile
    #     fields = ['email', 'first_name', 'last_name', 'role', 'department', 'password']
    #     widgets = {
    #         'password': forms.PasswordInput(),
    #     }

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name']

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


        
class AddTasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to']
        widgets = {
            'assigned_to': forms.HiddenInput(),
        }

