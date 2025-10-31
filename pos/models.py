from django.db import models
from django.contrib.auth.models import User
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