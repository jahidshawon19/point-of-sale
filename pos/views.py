from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from pos.models import Category, Product, Customer, Sale, SaleItem
from pos.forms import CategoryForm, ProductForm, CustomerForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
# Create your views here.

@login_required
def index(request):
    total_sales = Sale.objects.aggregate(total_amount_sum=Sum('total_amount'))['total_amount_sum'] or 0
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()

    context = {
        'total_sales': total_sales,
        'total_products': total_products,
        'total_customers': total_customers,
    }

    return render(request, 'pos/index.html', context)


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
        form = ProductForm(request.POST, request.FILES)
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



# Customer list with pagination and search
def customer_list(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(name__icontains=query) | Customer.objects.filter(mobile_no__icontains=query)
    else:
        customers = Customer.objects.all()
    
    paginator = Paginator(customers, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pos/customer_list.html', {'page_obj': page_obj, 'query': query})

# Add customer
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'pos/customer_form.html', {'form': form})

# Edit customer
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'pos/customer_form.html', {'form': form})

# Delete customer
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')
    return render(request, 'pos/customer_confirm_delete.html', {'customer': customer})




# Sales page
def sales_page(request):
    products = Product.objects.all()
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        product_ids = request.POST.getlist('product[]')
        quantities = request.POST.getlist('quantity[]')

        # Create Sale
        sale = Sale.objects.create(
            customer_id=customer_id,
            total_amount=0,
            date=timezone.now()
        )

        total_amount = 0

        for prod_id, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=prod_id)
            quantity = int(qty)
            unit_price = product.unitprice
            price = unit_price * quantity

            # Create SaleItem
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                price=price
            )

            # Reduce stock
            product.stock_quantity -= quantity
            product.save()

            total_amount += price

        # Update total amount
        sale.total_amount = total_amount
        sale.save()

        return redirect('invoice', sale_id=sale.id)

    return render(request, 'pos/sales.html', {'products': products, 'customers': customers})

# Invoice page
def invoice_page(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()  # related_name='items' in SaleItem
    return render(request, 'pos/invoice.html', {
        'sale': sale,
        'items': items
    })




def sales_record_list(request):
    sales = Sale.objects.order_by('-date')  # newest first
    return render(request, 'pos/sales_record.html', {'sales': sales})

def sales_record_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()  # related_name='items' in SaleItem
    return render(request, 'pos/sales_record_detail.html', {
        'sale': sale,
        'items': items
    })