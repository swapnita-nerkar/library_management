from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ['issue_date', 'return_date']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

USER=[
    ('admin', 'ADMIN'),
    ('students', 'Student'),
    ('other', 'Other'),
]
DEPARTMENTS = [
    ('it_dept', 'Information Technology Department'),
    ('cse_dept', 'Computer Science Department'),
    ('extc_dept', 'Electronics and Telecommunication Department'),
    ('mechanical_dept', 'MECHANICAL Department'),
    ('civil_dept', 'CIVIL Department'),
    ('textile_dept', 'TEXTILE Department'),
    ('other', 'Other'),
]
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    user = forms.CharField(max_length=50,widget=forms.Select(choices=USER))
    department = forms.CharField(max_length=50,widget=forms.Select(choices=DEPARTMENTS))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user', 'department', 'username', 'password1', 'password2')
