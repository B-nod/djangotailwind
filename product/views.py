from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from . forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse("Welcome to product page.")

def home(request):
    product = Product.objects.all()
    context = {
        "product": product
    }
    return render(request, 'products/index.html', context)

def addproduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Product added successfully !")
            return redirect('/products/addproduct')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify product field.')
            return render(request,'products/addproduct.html',{'form':form})
    
    context ={
        'form':ProductForm
    }
    return render(request, 'products/addproduct.html', context)

def updateproduct(request, product_id):
    instance = Product.objects.get(id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product updated succesfully')
            return redirect('/products/home')
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields')
            return render(request, 'products/updateproduct.html', {'form':form})
    

    context = {
        'form':ProductForm(instance=instance)
    }
    return render(request, 'products/updateproduct.html', context)

def deleteproduct(request, product_id):
    instance = Product.objects.get(id=product_id)
    instance.delete()
    messages.add_message(request, messages.ERROR, 'Product deleted successfully')
    return redirect('/products/home')

def categorylist(request):
    category = Category.objects.all().order_by('-id')
    context = {
        'category':category
    }
    return render(request, 'products/categorylist.html', context)

def addcategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category added successfully !")
            return redirect('/products/addcategory')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify product field.')
            return render(request,'products/addcategory.html',{'form':form})
    
    context ={
        'form':CategoryForm
    }
    return render(request, 'products/addcategory.html', context)

def updatecategory(request, category_id):
    instance = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated succesfully')
            return redirect('/products/categorylist')
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields')
            return render(request, 'products/updatecategory.html', {'form':form})
    

    context = {
        'form':CategoryForm(instance=instance)
    }
    return render(request, 'products/updatecategory.html', context)

def deletecategory(request, category_id):
    instance = Category.objects.get(id=category_id)
    instance.delete()
    messages.add_message(request, messages.ERROR, 'Category deleted successfully')
    return redirect('/products/categorylist')