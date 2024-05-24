from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    delivery = models.CharField(max_length=100)
    actual_price = models.CharField(max_length=200)
    discounted_price = models.CharField(max_length=200)
    
    def __str__(self):
        return self.product_name
 
    
    # def clean(self):
    #     if self.actual_price < 0 or self.discounted_price < 0:
    #         raise ValidationError('Prices must be positive.')
    #     if self.discounted_price > self.actual_price:
    #         raise ValidationError('Discounted price must be less than or equal to the actual price.')