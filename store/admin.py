from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Category, Product, HeroBanner, CartItem, Order, OrderItem, DeliveryOption, ProductImage

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create a better hierarchy display for parent selection
        choices = [('', '--- Root Category (No Parent) ---')]
        
        # Get all root categories and build the tree
        for category in Category.objects.filter(parent=None).order_by('name'):
            # Skip current category to prevent self-reference
            if self.instance and self.instance.pk == category.pk:
                continue
            choices.append((category.pk, category.name))
            self._add_children(category, choices, level=1)
        
        self.fields['parent'].choices = choices
        self.fields['parent'].widget.attrs.update({
            'class': 'form-control',
            'style': 'font-family: monospace; min-height: 200px;'
        })
    
    def _add_children(self, category, choices, level=0):
        """Recursively add children with proper indentation"""
        indent = '├' + '─' * level + ' '
        for child in category.children.all().order_by('name'):
            # Skip current category and its descendants to prevent circular reference
            if self.instance and (self.instance.pk == child.pk or self._is_descendant(child)):
                continue
            choices.append((child.pk, f'{indent}{child.name}'))
            self._add_children(child, choices, level + 1)
    
    def _is_descendant(self, category):
        """Check if category is a descendant of current instance"""
        if not self.instance or not self.instance.pk:
            return False
        parent = category.parent
        while parent:
            if parent.pk == self.instance.pk:
                return True
            parent = parent.parent
        return False
    
    def clean_parent(self):
        """Validate parent selection to prevent circular references"""
        parent = self.cleaned_data.get('parent')
        if parent and self.instance and self.instance.pk:
            # Check if trying to set self as parent
            if parent.pk == self.instance.pk:
                raise forms.ValidationError("A category cannot be its own parent.")
            
            # Check if trying to set a descendant as parent
            if self._is_descendant_of_instance(parent):
                raise forms.ValidationError("Cannot set a descendant category as parent.")
        
        return parent
    
    def _is_descendant_of_instance(self, category):
        """Check if category is a descendant of current instance"""
        current = category.parent
        while current:
            if current.pk == self.instance.pk:
                return True
            current = current.parent
        return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['indented_name', 'slug', 'get_level', 'products_count', 'created_at']
    search_fields = ['name', 'slug']
    list_filter = ['created_at', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['parent__name', 'name']
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
    
    def indented_name(self, obj):
        """Display category name with indentation based on level"""
        level = obj.get_level()
        indent = '—' * level + ' ' if level > 0 else ''
        level_class = f'level-{level}'
        return format_html(f'<span class="{level_class}">{indent}{obj.name}</span>')
    indented_name.short_description = 'Category Name'
    
    def get_level(self, obj):
        """Display the hierarchy level"""
        return obj.get_level()
    get_level.short_description = 'Level'
    
    def products_count(self, obj):
        """Display number of products in this category"""
        return obj.products.count()
    products_count.short_description = 'Products'

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
