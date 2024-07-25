from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    
    date_range = forms.CharField(widget=forms.TextInput())
    
    class Meta:
        model = Application
        fields = ['hall', 'name', 'director', 'email', 'phone_number', 'account_number', 'inn', 'address']