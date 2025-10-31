from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from pos.models import Category, Product
from pos.forms import CategoryForm, ProductForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render (request , 'pos/index.html')


@login_required
def category_list(request):
    """List all categories with search functionality."""
    search_query = request.GET.get('search', '')
    if search_query:
        categories = Category.objects.filter(name__icontains=search_query)
    else:
        categories = Category.objects.all()
    return render(request, 'pos/category_list.html', {'categories': categories, 'search_query': search_query})


@login_required
def category_create(request):
    """Create a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.updated_by = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'pos/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def category_update(request, pk):
    """Update an existing category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.updated_by = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'pos/category_form.html', {'form': form, 'title': 'Edit Category'})


@login_required
def category_delete(request, pk):
    """Delete a category."""
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')





@login_required
def product_list(request):
    """List all products with search functionality."""
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(
            name__icontains=search_query
        )
    else:
        products = Product.objects.all()
    return render(request, 'pos/product_list.html', {'products': products, 'search_query': search_query})


@login_required
def product_create(request):
    """Create a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.updated_by = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'pos/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_update(request, pk):
    """Update an existing product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_by = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'pos/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def product_delete(request, pk):
    """Delete a product."""
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')
