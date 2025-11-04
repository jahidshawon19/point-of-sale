from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


# CATEGORY MODEL # 

#id, name, created_date, updated_date, created_by, updated_by

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_created_by'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_updated_by'
    )


    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# PRODUCT MODEL # 

#id, name, image, category , unitprice, stock_quantity, created_date, updated_date, created_by, updated_by

class Product(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='product_created_by'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='product_updated_by'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def stock_status(self):
        """Quick stock indicator."""
        if self.stock_quantity == 0:
            return "Out of Stock"
        elif self.stock_quantity <= 5:
            return "Low Stock"
        return "In Stock"
    


# customer models


class Customer(models.Model):

    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"