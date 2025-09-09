from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, HeroBanner, CartItem, Order, OrderItem, DeliveryOption, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'display_price', 'stock_quantity', 'is_best_seller', 'is_featured', 'is_in_stock']
    list_filter = ['category', 'is_best_seller', 'is_featured', 'created_at']
    search_fields = ['name', 'slug', 'description']
    list_editable = ['stock_quantity', 'is_best_seller', 'is_featured']
    list_per_page = 20
    fields = ['name', 'slug', 'description', 'category', 'image', 'youtube_url', 'original_price', 'price', 'stock_quantity', 'is_best_seller', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    
    def display_price(self, obj):
        if obj.has_discount:
            return format_html(
                '<span style="text-decoration: line-through; color: #666;">৳{}</span> '
                '<span style="color: #28a745; font-weight: bold;">৳{}</span> '
                '<span style="background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}% OFF</span>',
                obj.original_price, obj.price, obj.discount_percentage
            )
        return f'৳{obj.price}'
    display_price.short_description = 'Price'

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    ordering = ['order', '-created_at']

@admin.register(DeliveryOption)
class DeliveryOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['price', 'is_active', 'order']
    ordering = ['order', 'price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'product', 'quantity', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session_key', 'product__name']
    readonly_fields = ['total_price']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['total_price']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'customer_phone', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_id', 'customer_name', 'customer_phone']
    list_editable = ['status']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'payment_method', 'subtotal', 'delivery_option', 'delivery_fee', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'shipping_address')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        })
    )
    
    # def has_delete_permission(self, request, obj=None):
    #     # Prevent deletion of confirmed orders
    #     if obj and obj.status in ['confirmed', 'shipped', 'delivered']:
    #         return False
    #     return True


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_featured', 'order', 'created_at']
    list_filter = ['product', 'is_featured', 'created_at']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['is_featured', 'order']
    ordering = ['product', 'order']


# Customize admin site appearance
admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Admin"
admin.site.index_title = "Welcome to E-Commerce Administration"
