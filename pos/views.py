from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from pos.models import Category, Product, Customer, Sale, SaleItem
from pos.forms import CategoryForm, ProductForm, CustomerForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages




# Create my views here.

@login_required
def index(request):
    # Summary totals
    total_sales = Sale.objects.aggregate(total_amount_sum=Sum('total_amount'))['total_amount_sum'] or 0
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    

    # Daily sales (last 7 days)
    daily_sales_qs = (
        Sale.objects
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(total=Sum('total_amount'))
        .order_by('day')
    )
    daily_labels = [d['day'].strftime('%b %d') for d in daily_sales_qs]
    daily_values = [float(d['total']) for d in daily_sales_qs]

    # Monthly sales (this year)
    monthly_sales_qs = (
        Sale.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )
    monthly_labels = [m['month'].strftime('%b %Y') for m in monthly_sales_qs]
    monthly_values = [float(m['total']) for m in monthly_sales_qs]

    return render(request, 'pos/index.html', {
        'total_sales': total_sales,
        'total_products': total_products,
        'total_customers': total_customers,
        'daily_labels': daily_labels,
        'daily_values': daily_values,
        'monthly_labels': monthly_labels,
        'monthly_values': monthly_values,
    })


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
@login_required
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
@login_required
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
@login_required
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
@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')
    return render(request, 'pos/customer_confirm_delete.html', {'customer': customer})



@login_required
def sales_page(request):
    # Only show products that are in stock
    products = Product.objects.filter(stock_quantity__gt=0)
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        product_ids = request.POST.getlist('product[]')
        quantities = request.POST.getlist('quantity[]')
        discount_percent = Decimal(request.POST.get('discount') or 0)
        vat_percent = Decimal(request.POST.get('vat') or 0)

        # Create Sale
        sale = Sale.objects.create(
            customer_id=customer_id,
            total_amount=Decimal('0.00'),
            date=timezone.now(),
            discount=discount_percent,
            vat=vat_percent,
            created_by=request.user
        )

        total_amount = Decimal('0.00')

        for prod_id, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=prod_id)
            quantity = int(qty)

            # ✅ Check stock before creating SaleItem
            if quantity > product.stock_quantity:
                messages.error(
                    request,
                    f"Cannot sell {quantity} × {product.name}. Only {product.stock_quantity} left in stock."
                )
                # Delete partially created sale
                sale.delete()
                return redirect('sales')

            unit_price = product.unitprice
            price = Decimal(unit_price) * quantity

            # Create SaleItem
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                price=price
            )

            # Reduce stock safely
            product.stock_quantity -= quantity
            product.save()

            total_amount += price

        # Apply discount and VAT
        discount_amount = total_amount * (discount_percent / Decimal('100'))
        vat_amount = (total_amount - discount_amount) * (vat_percent / Decimal('100'))
        grand_total = total_amount - discount_amount + vat_amount

        # Update sale totals
        sale.total_amount = grand_total
        sale.save()

        return redirect('invoice', sale_id=sale.id)

    return render(request, 'pos/sales.html', {'products': products, 'customers': customers})




# Invoice page
@login_required
def invoice_page(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()  # related_name='items' in SaleItem
    return render(request, 'pos/invoice.html', {
        'sale': sale,
        'items': items
    })


@login_required
def sales_record_list(request):
    sales = Sale.objects.all().select_related('customer', 'created_by').order_by('-date')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        sales = sales.filter(date__date__range=[start_date, end_date])
    elif start_date:
        sales = sales.filter(date__date__gte=start_date)
    elif end_date:
        sales = sales.filter(date__date__lte=end_date)

    return render(request, 'pos/sales_record.html', {'sales': sales})


@login_required
def sales_record_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()  # related_name='items' in SaleItem
    return render(request, 'pos/sales_record_detail.html', {
        'sale': sale,
        'items': items
    })



@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    from .forms import CreateUserForm
    from django.contrib import messages
    from django.contrib.auth.models import User

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('index')
    else:
        form = CreateUserForm()

    return render(request, 'pos/create_user.html', {'form': form})
