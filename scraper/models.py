from django.db import models
from mongoengine import *
# Create your models here.



class Datatable(models.Model):

    Title = models.CharField('Title',max_length=500),
    Price = models.DecimalField('Price',decimal_places = 3, max_digits = 10000),
    Currency = models.CharField('Currency',max_length=500),
    Stars = models.DecimalField('Stars',decimal_places = 3 , max_digits = 10000),
    Orders = models.PositiveIntegerField('Orders',max_length=500),
    Shipcost = models.CharField('Shipcost',max_length=500),
    Supplier = models.CharField('Supplier',max_length=500),
    Productlinks = models.CharField('Productlinks',max_length=700)