from django.db import models
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __self__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product-list', args=[self.pk])

    class Meta:
        ordering = ['name',]


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        'ProductType',
        on_delete = models.CASCADE,
    )
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=100)

    def __self__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product-detail', args=[self.pk])

    class Meta:
        ordering = ['name',]
