from django.urls import path
from . import views
from .analytics_views import analytics_dashboard, product_analytics, order_analytics

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('track-order/', views.track_order, name='track_order'),
    path('track/<str:tracking_number>/', views.order_tracking_details, name='order_tracking_details'),
    path('contact/', views.contact, name='contact'),
    
    # Policy and Info Pages
    path('about/', views.about, name='about'),
    path('return-refund/', views.return_refund, name='return_refund'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    
    # Analytics URLs
    path('analytics/', analytics_dashboard, name='analytics_dashboard'),
    path('analytics/products/', product_analytics, name='product_analytics'),
    path('analytics/orders/', order_analytics, name='order_analytics'),
]
