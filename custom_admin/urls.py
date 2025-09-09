from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:product_slug>/delete/', views.product_delete, name='product_delete'),
    
    # Product Images
    path('product-images/<int:image_id>/delete/', views.product_image_delete, name='product_image_delete'),
    path('product-images/reorder/', views.product_image_reorder, name='product_image_reorder'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('categories/<slug:category_slug>/delete/', views.category_delete, name='category_delete'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    
    # Banners
    path('banners/', views.banner_management, name='banner_management'),
    path('banners/create/', views.banner_create, name='banner_create'),
    path('banners/<int:banner_id>/', views.banner_detail, name='banner_detail'),
    path('banners/<int:banner_id>/delete/', views.banner_delete, name='banner_delete'),
    path('banners/reorder/', views.banner_reorder, name='banner_reorder'),
    
    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),
    
    # Settings
    path('settings/', views.settings_view, name='settings'),
    
    # Featured Products
    path('featured/', views.featured_products, name='featured_products'),
    
    # Profile
    path('profile/', views.admin_profile, name='profile'),
    
    # Auth
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # DeliveryOption management
    path('delivery-options/', views.deliveryoption_list, name='deliveryoption_list'),
    path('delivery-options/add/', views.deliveryoption_add, name='deliveryoption_add'),
    path('delivery-options/<int:pk>/edit/', views.deliveryoption_edit, name='deliveryoption_edit'),
    path('delivery-options/<int:pk>/delete/', views.deliveryoption_delete, name='deliveryoption_delete'),
    # AJAX endpoints
    path('ajax/order-status/', views.quick_status_update, name='quick_status_update'),
]
