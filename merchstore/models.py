from django.db import models
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name',]

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        'ProductType',
        on_delete = models.SET_NULL,
    )
    description = models.TextField()
    price = models.DecimalField(decimal_places=2)

    class Meta:
        ordering = ['name',]
