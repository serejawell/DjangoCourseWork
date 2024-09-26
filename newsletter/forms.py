from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", max_length=100)
    last_name = forms.CharField(label="Фамилия", max_length=100)
    middle_name = forms.CharField(label="Отчество", max_length=100, required=False)
    email = forms.EmailField(label="Email", max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email']
