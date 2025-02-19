from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.FileField(upload_to='static/uploads',null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
class Order(models.Model):
    PAYMENT = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Esewa', 'Esewa'),
        ('Khalti', 'Khalti')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    contact_no = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200,choices=PAYMENT)
    payment_status = models.BooleanField(default=False)

    

