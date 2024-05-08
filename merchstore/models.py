from django.db import models
from django.urls import reverse

from user_management import models as ProfileModels

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'merchstore:product-list',
             args=[self.pk])

    class Meta:
        ordering = ['name',]


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        'ProductType',
        on_delete = models.SET_NULL,
        related_name = 'products',
        null = True,
    )
    owner = models.ForeignKey(
        ProfileModels.Profile,
        on_delete = models.CASCADE,
        related_name = 'products'
    )
    
    description = models.TextField()
    price = models.DecimalField(
        decimal_places=2, 
        max_digits=100)
    stock = models.PositiveIntegerField()
    status = models.CharField(
        max_length=12, 
        choices=(('Available','Available'), 
                 ('On sale', 'On sale'), 
                 ('Out of stock','Out of stock'),),
                 default='Available')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'merchstore:product-detail', 
            args=[self.pk])

    class Meta:
        ordering = ['name',]

class Transaction(models.Model):
    buyer = models.ForeignKey(
        ProfileModels.Profile,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'transactions'
    )
    product = models.ForeignKey(
        'Product',
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'transactions'
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, 
        choices=(('On cart','On cart'), 
                 ('To pay', 'To pay'), 
                 ('To ship','To ship'), 
                 ('To receive','To receive'), 
                 ('Delivered','Delivered'),))
    created_on = models.DateTimeField(
        auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on',]
