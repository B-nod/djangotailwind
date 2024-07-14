from django.db import models

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
    
    

