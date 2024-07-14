from django.shortcuts import render
from product.models import *

# Create your views here.
def homepage(request):
    product = Product.objects.all()[:8]
    context = {
        'product':product
    }
    return render(request, 'users/home.html', context)
