
from django import forms
from django.forms import ModelForm
from polls.models import  MyModel

class MyForm(ModelForm):
    name = forms.CharField(label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)

def clean_name(self):
    name = self.cleaned_data.get('name')
    if not name:
        raise forms.ValidationError("Please enter your name.")
    return name

def clean_email(self):
    email = self.cleaned_data.get('email')
    if not email:
        raise forms.ValidationError("Please enter your email.")
    return email


