from django.shortcuts import render, redirect
from product.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . forms import *
from django.contrib import messages
# Create your views here.
def homepage(request):
    product = Product.objects.all()[:8]
    context = {
        'product':product
    }
    return render(request, 'users/home.html', context)

def productdetail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product':product
    }
    return render(request, 'users/productdetail.html', context)

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.add_message, 'Account Created Successfully')
            return redirect('/registers')
        else:
            messages.add_message(request, messages.add_message, 'Kindly input valid credantials')
            return render(request, 'users/register.html', {'form':form})
    
    context = {
        'form':UserCreationForm
    }
    return render(request,'users/register.html', context)

def user_login(request):

    context = {
        'form':LoginForm
    }
    return render(request, 'users/login.html', context)