from django.db import models
from django.urls import reverse

from user_management import models as ProfileModels

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product-list', args=[self.pk])

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
    price = models.DecimalField(decimal_places=2, max_digits=100)
    stock = models.PositiveIntegerField()

    class States(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        AVAILABLE = 'Available', 'Available'
        ON_SALE = 'On sale', 'On sale'
        OUT_OF_STOCK = 'Out of stock', 'Out of stock'
    
    status = models.CharField(
        max_length = 12,
        choices = States,
        default = States.AVAILABLE
    )
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product-detail', args=[self.pk])

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

    class States(models.TextChoices):
        ONCART = 'On cart', 'On cart'
        TOPAY = 'To pay', 'To pay'
        TOSHIP = 'To ship', 'To ship'
        TORECEIVE = 'To receive', 'To receive'
        DELIVERED = 'Delivered', 'Delivered'
    
    status = models.CharField(
        max_length = 10,
        choices = States)
    created_on = models.DateTimeField(auto_now_add=True)
