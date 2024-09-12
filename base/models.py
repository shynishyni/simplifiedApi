from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0, blank=True, null=True)
    longitude = models.FloatField(default=0, blank=True, null=True)
    city = models.CharField(default="null", max_length=200,blank=True, null=True)
    country = models.CharField(default="null", max_length=200,blank=True, null=True)
    favorites = models.JSONField(default=list)
    cart = models.JSONField(default=list)
    landmark = models.CharField(default="null",max_length=250,blank=True,null=True)
    pincode = models.CharField(default="null",max_length=250,blank=True,null=True)
    address = models.CharField(default="null",max_length=250,blank=True,null=True)
    number = models.CharField(default=0, max_length=10, blank=True,null=True)
    item_ordered=models.JSONField(default=list)
    def __str__(self):
        return self.user.username
    
class Item(models.Model):
    username=models.CharField(max_length=200,default='some_default_value')
    emailid = models.EmailField(max_length=200,default='some_default_value')
    password = models.CharField(max_length=200,default='some_default_value')
    confirmpassword = models.CharField(max_length=200, default='some_default_value')
    created=models.DateTimeField(auto_now_add=True)
    lat=models.FloatField(default='0')
    long=models.FloatField(default='0')
    city=models.CharField(max_length=255,default="null")
    country=models.CharField(max_length=255,default="null")

class Product(models.Model):
    name = models.CharField(max_length=255)
    original_cost = models.DecimalField(max_digits=10, decimal_places=2)
    offer_percent = models.IntegerField(blank=True, null=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    size = models.CharField(max_length=10, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')])
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    stars = models.IntegerField(blank=True, null=True)
    num_sales = models.IntegerField(blank=True, null=True)
    sizes_available = models.CharField(max_length=255, blank=True, null=True)
    colors_available = models.CharField(max_length=255, blank=True, null=True)
    dimensions = models.CharField(max_length=20, blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    num_in_stock = models.IntegerField(blank=True, null=True)
    related_sports = models.CharField(max_length=255, blank=True, null=True)
    pictures = models.ImageField(upload_to='products/', blank=True, null=True)
