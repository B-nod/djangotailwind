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
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'], password = ['password'])
            if user is not None:
                return redirect('/')
            else:
                return render(request, 'users/login.html', {'form':form})


    context = {
        'form':LoginForm
    }
    return render(request, 'users/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('/login')

@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_items_present = Cart.objects.filter(user=user, product=product)
    if check_items_present:
        messages.add_message(request, messages.ERROR, 'Product was already present in cart')
        return redirect('/productpage')
    else:
        cart = Cart.objects.create(product=product, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Product added successfully in carts')
            return redirect('/cart')
        else:
            messages.add_message(request, messages.ERROR, 'Some Error occure')

@login_required
def viewcart(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items':items
    }
    return render(request, 'users/cart.html', context)

@login_required
def deletecart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.ERROR, 'product removed from cart')
    return redirect('/cart')

@login_required
def order(request, product_id, cart_id):
    user=request.user
    products = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        price = products.product_price
        quantity = request.POST.get('quantity')
        total_price = int(price)*int(quantity)
        payment_method = request.POST.get('payment_method')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
      
        order = Order.objects.create(
            product=products,
            user=user,
            quantity=quantity,
            total_price=total_price,
            payment_method=payment_method,
            contact_no=contact_no,
            address=address,
           
        )
        if order.payment_method == 'Cash on Delivery':
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Provide cash when delivery')
            return redirect('/myorder')
        elif order.payment_method == 'Esewa':
            return redirect(reverse('esewaform')+"?o_id="+str(order.id)+"&c_id="+str(cart.id))
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verfiy all fields')
            return render(request, 'users/order.html', {"form":form})

    context = {
        'form':OrderForm
    }
    return render(request, 'users/order.html', context)

@login_required
def myorder(request):
    order = Order.objects.all()
    context = {
        "order":order
    }
    return render(request, 'users/myorder.html', context)



import hmac #cryptography algorithm
import hashlib #encrypt data
import uuid  #to generate random string 
import base64
class EsewaView(View):
   def get(self,request,*args,**kwargs):
        o_id=request.GET.get('o_id')
        c_id=request.GET.get('c_id')
        cart=Cart.objects.get(id=c_id)
        order=Order.objects.get(id=o_id)
        
        
        uuid_val=uuid.uuid4()
        
        def genSha256(key,message):
            key=key.encode('utf-8')
            message=message.encode('utf-8')

            hmac_sha256=hmac.new(key,message,hashlib.sha256)

            digest=hmac_sha256.digest()

            signature=base64.b64encode(digest).decode('utf-8')
            return signature
        
        secret_key='8gBm/:&EnhH.1/q'
        data_to_sign=f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
        
        result=genSha256(secret_key,data_to_sign)

        data={
            'amount':order.product.product_price,
            'total_amount':order.total_price,
            'transaction_uuid':uuid_val,
            'product_code':'EPAYTEST',
            'signature':result,
        }
        context={
            'order':order,
            'data':data,
            'cart':cart
        }
        return render(request,'users/esewa_payment.html',context)

import json
@login_required
def esewa_verify(request, order_id, cart_id):
    if request.method == 'GET':
        data = request.GET.get('data')
        decoded_data = base64.b64decode(data).decode('utf-8')
        map_data = json.loads(decoded_data)
        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(id=cart_id)
        
        if map_data.get('status') == 'COMPLETE':
            order.payment_status = True
            order.save()
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Payment Successful')
            return redirect('/myorder')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to make a payment')
            return redirect('/my_order')
        
@login_required
def user_profile(request):
    user = request.user
 
    return render(request,'users/profile.html')
    
