from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug'], name='category_slug_idx'),
            models.Index(fields=['name'], name='category_name_idx'),
            models.Index(fields=['created_at'], name='category_created_idx'),
        ]
    
    def save(self, *args, **kwargs):
        # Always regenerate slug when name changes or when slug is empty
        if not self.slug or self.pk:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Exclude current instance from uniqueness check
            queryset = Category.objects.filter(slug=slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            while queryset.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                queryset = Category.objects.filter(slug=slug)
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_products', kwargs={'category_slug': self.slug})

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True, help_text='Original price before discount')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    youtube_url = models.URLField(blank=True, null=True, help_text='YouTube video URL for this product')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_best_seller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug'], name='product_slug_idx'),
            models.Index(fields=['category'], name='product_category_idx'),
            models.Index(fields=['stock_quantity'], name='product_stock_idx'),
            models.Index(fields=['is_best_seller'], name='product_bestseller_idx'),
            models.Index(fields=['is_featured'], name='product_featured_idx'),
            models.Index(fields=['price'], name='product_price_idx'),
            models.Index(fields=['created_at'], name='product_created_idx'),
            models.Index(fields=['name'], name='product_name_idx'),
            # Composite indexes for common query patterns
            models.Index(fields=['category', 'stock_quantity'], name='product_cat_stock_idx'),
            models.Index(fields=['is_best_seller', 'stock_quantity'], name='product_best_stock_idx'),
            models.Index(fields=['is_featured', 'stock_quantity'], name='product_feat_stock_idx'),
        ]
    
    def save(self, *args, **kwargs):
        # Always regenerate slug when name changes or when slug is empty
        if not self.slug or self.pk:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Exclude current instance from uniqueness check
            queryset = Product.objects.filter(slug=slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            while queryset.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                queryset = Product.objects.filter(slug=slug)
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'product_slug': self.slug})
    
    def get_youtube_embed_url(self):
        """Extract YouTube video ID and return embed URL"""
        if not self.youtube_url:
            return None
        
        import re
        # Extract video ID from various YouTube URL formats
        patterns = [
            r'youtube\.com/watch\?v=([^&]+)',
            r'youtube\.com/embed/([^?]+)',
            r'youtu\.be/([^?]+)',
            r'youtube\.com/v/([^?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                video_id = match.group(1)
                return f'https://www.youtube.com/embed/{video_id}'
        
        return None
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def has_discount(self):
        """Check if product has a discount (original price > current price)"""
        return self.original_price and self.original_price > self.price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if not self.has_discount:
            return 0
        return int(((self.original_price - self.price) / self.original_price) * 100)
    
    @property
    def savings_amount(self):
        """Calculate savings amount"""
        if not self.has_discount:
            return 0
        return self.original_price - self.price

class HeroBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['is_active'], name='herobanner_active_idx'),
            models.Index(fields=['order'], name='herobanner_order_idx'),
            models.Index(fields=['created_at'], name='herobanner_created_idx'),
        ]
    
    def __str__(self):
        return self.title

class DeliveryOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'price']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class CartItem(models.Model):
    session_key = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session_key', 'product']
        indexes = [
            models.Index(fields=['session_key'], name='cartitem_session_idx'),
            models.Index(fields=['product'], name='cartitem_product_idx'),
            models.Index(fields=['created_at'], name='cartitem_created_idx'),
            # Composite index for cart operations
            models.Index(fields=['session_key', 'product'], name='cartitem_session_product_idx'),
        ]
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=20, unique=True)
    tracking_number = models.CharField(max_length=20, unique=True, blank=True)  # Same as order_id for simplicity
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, default='cod')  # Cash on Delivery
    notes = models.TextField(blank=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_id'], name='order_id_idx'),
            models.Index(fields=['status'], name='order_status_idx'),
            models.Index(fields=['created_at'], name='order_created_idx'),
            models.Index(fields=['customer_name'], name='order_customer_idx'),
            models.Index(fields=['customer_email'], name='order_email_idx'),
            models.Index(fields=['customer_phone'], name='order_phone_idx'),
            # Composite indexes for common admin queries
            models.Index(fields=['status', 'created_at'], name='order_status_created_idx'),
        ]
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate order ID
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.order_id = f"ORD{timestamp}"
        if not self.tracking_number:
            self.tracking_number = self.order_id  # Use order_id as tracking number
        super().save(*args, **kwargs)
    
    def get_status_display_with_icon(self):
        """Get status with appropriate icon"""
        status_icons = {
            'pending': 'bi-clock',
            'confirmed': 'bi-check-circle',
            'processing': 'bi-gear',
            'shipped': 'bi-truck',
            'out_for_delivery': 'bi-geo-alt',
            'delivered': 'bi-check-circle-fill',
            'cancelled': 'bi-x-circle',
        }
        return {
            'status': self.get_status_display(),
            'icon': status_icons.get(self.status, 'bi-circle')
        }
    
    def get_status_progress(self):
        """Get progress percentage based on status"""
        progress_map = {
            'pending': 10,
            'confirmed': 25,
            'processing': 40,
            'shipped': 65,
            'out_for_delivery': 85,
            'delivered': 100,
            'cancelled': 0,
        }
        return progress_map.get(self.status, 0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    class Meta:
        indexes = [
            models.Index(fields=['order'], name='orderitem_order_idx'),
            models.Index(fields=['product'], name='orderitem_product_idx'),
        ]
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity


class OrderStatusHistory(models.Model):
    """Track order status changes for detailed tracking"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    notes = models.TextField(blank=True, help_text='Additional notes about this status change')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, default='System', help_text='Who made this change')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Order Status Histories'
    
    def __str__(self):
        return f"{self.order.order_id} - {self.get_status_display()} at {self.created_at}"


class SiteSettings(models.Model):
    """Site branding and configuration settings"""
    site_name = models.CharField(max_length=100, default='E-Store')
    site_tagline = models.CharField(max_length=200, blank=True, help_text='Short tagline for your store')
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text='Site logo')
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True, help_text='Site favicon')
    
    # Header colors
    header_bg_color = models.CharField(max_length=7, default='#0d6efd', help_text='Header background color (hex)')
    header_text_color = models.CharField(max_length=7, default='#ffffff', help_text='Header text color (hex)')
    
    # Contact information
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Social media links
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True, help_text='Site meta description for SEO')
    meta_keywords = models.CharField(max_length=200, blank=True, help_text='Comma-separated keywords')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f'Site Settings - {self.site_name}'
    
    @classmethod
    def get_current(cls):
        """Get the current site settings, create if doesn't exist"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class UserVisit(models.Model):
    """Track user visits for analytics"""
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    page_visited = models.CharField(max_length=255, blank=True)
    
    class Meta:
        unique_together = ['session_key', 'date']
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['date'], name='uservisit_date_idx'),
            models.Index(fields=['session_key'], name='uservisit_session_idx'),
            models.Index(fields=['ip_address'], name='uservisit_ip_idx'),
            models.Index(fields=['timestamp'], name='uservisit_timestamp_idx'),
        ]
    
    def __str__(self):
        return f'Visit on {self.date} - {self.ip_address}'


class OnlineUser(models.Model):
    """Track currently online users"""
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    last_activity = models.DateTimeField(auto_now=True)
    user_agent = models.TextField(blank=True)
    current_page = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['session_key'], name='onlineuser_session_idx'),
            models.Index(fields=['last_activity'], name='onlineuser_activity_idx'),
            models.Index(fields=['ip_address'], name='onlineuser_ip_idx'),
        ]
    
    def __str__(self):
        return f'Online: {self.ip_address} - {self.last_activity}'
