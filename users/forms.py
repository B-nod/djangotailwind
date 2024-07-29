
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
  
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', 'contact_no', 'address', 'quantity']