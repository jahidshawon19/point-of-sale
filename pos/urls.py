from django.urls import path
from pos import views 

urlpatterns = [
    path('', views.index, name='index'),
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Product URLs (example)
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Customer URLS
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_add'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    path('sales/', views.sales_page, name='sales'),
    path('invoice/<int:sale_id>/', views.invoice_page, name='invoice'),

    path('sales-records/', views.sales_record_list, name='sales_record_list'),
    path('sales-records/<int:sale_id>/', views.sales_record_detail, name='sales_record_detail'),
]
