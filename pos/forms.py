from django import forms
from pos.models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            })
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'category', 'unitprice', 'stock_quantity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'unitprice': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unit price'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity'
            }),
        }
