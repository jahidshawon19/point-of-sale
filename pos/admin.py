from django.contrib import admin
from .models import Category, Product, Customer,Sale
from django.utils.html import format_html

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile_no', 'created_at', 'updated_at')
    list_filter = ('name', 'mobile_no')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'updated_by', 'created_date', 'updated_date')
    list_filter = ('created_date', 'updated_date')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = (
        ("Category Information", {
            "fields": ("name",)
        }),
        ("Audit Information", {
            "fields": ("created_by", "updated_by", "created_date", "updated_date")
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'formatted_price',
        'stock_quantity', 'colored_stock_status',
        'created_by', 'updated_by', 'created_date', 'updated_date'
    )
    list_filter = ('category', 'created_date', 'updated_date')
    search_fields = ('name', 'category__name')
    ordering = ('name',)
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = (
        ("Product Information", {
            "fields": ("name", "image", "category", "unitprice", "stock_quantity")
        }),
        ("Audit Information", {
            "fields": ("created_by", "updated_by", "created_date", "updated_date")
        }),
    )

    def formatted_price(self, obj):
        return f"${obj.unitprice:,.2f}"
    formatted_price.short_description = "Unit Price"

    def colored_stock_status(self, obj):
        """Show color-coded stock status in admin list."""
        status = obj.stock_status
        if status == "Out of Stock":
            color = "red"
        elif status == "Low Stock":
            color = "orange"
        else:
            color = "green"
        return format_html('<b><span style="color: {};">{}</span></b>', color, status)
    colored_stock_status.short_description = "Stock Status"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'date', 'created_by')
    list_filter = ('date', 'created_by')