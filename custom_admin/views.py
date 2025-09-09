
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import json

from store.models import Product, Category, Order, OrderItem, HeroBanner, SiteSettings, UserVisit, OnlineUser, OrderStatusHistory, DeliveryOption, ProductImage

# Check if user is staff
def is_staff(user):
    return user.is_authenticated and user.is_staff

# Custom decorator for admin views
def admin_required(view_func):
    """Decorator that requires user to be authenticated and staff"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_admin:login')
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access the admin panel.')
            return redirect('custom_admin:login')
        return view_func(request, *args, **kwargs)
    return wrapper

# DeliveryOption Management Views
@admin_required
def deliveryoption_list(request):
    options = DeliveryOption.objects.all()
    return render(request, 'custom_admin/deliveryoption_list.html', {'options': options})

@admin_required
def deliveryoption_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0').strip()
        is_active = bool(request.POST.get('is_active', False))
        order = request.POST.get('order', '0').strip()
        if name and price:
            option = DeliveryOption(
                name=name,
                description=description,
                price=price,
                is_active=is_active,
                order=order
            )
            option.save()
            messages.success(request, 'Delivery option added.')
            return redirect('custom_admin:deliveryoption_list')
        else:
            messages.error(request, 'Name and price are required.')
    return render(request, 'custom_admin/deliveryoption_add.html')

@admin_required
def deliveryoption_edit(request, pk):
    option = get_object_or_404(DeliveryOption, pk=pk)
    if request.method == 'POST':
        option.name = request.POST.get('name', option.name)
        option.description = request.POST.get('description', option.description)
        option.price = request.POST.get('price', option.price)
        option.is_active = bool(request.POST.get('is_active', option.is_active))
        option.order = request.POST.get('order', option.order)
        option.save()
        messages.success(request, 'Delivery option updated.')
        return redirect('custom_admin:deliveryoption_list')
    return render(request, 'custom_admin/deliveryoption_edit.html', {'option': option})

@admin_required
def deliveryoption_delete(request, pk):
    option = get_object_or_404(DeliveryOption, pk=pk)
    if request.method == 'POST':
        option.delete()
        messages.success(request, 'Delivery option deleted.')
        return redirect('custom_admin:deliveryoption_list')
    return render(request, 'custom_admin/deliveryoption_delete.html', {'option': option})

@admin_required
def admin_dashboard(request):
    """Main dashboard view with overview statistics"""
    
    # Basic statistics
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_categories = Category.objects.count()
    
    # Revenue calculations
    total_revenue = Order.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Visit statistics
    today = timezone.now().date()
    today_visits = UserVisit.objects.filter(date=today).count()
    current_online = OnlineUser.objects.count()
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Top selling products
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by('-total_sold')[:5]
    
    # Low stock alerts
    low_stock_products = Product.objects.filter(stock_quantity__lt=10)
    
    # Monthly sales data for chart
    monthly_sales = []
    for i in range(12):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=31)
        month_revenue = Order.objects.filter(
            created_at__range=[month_start, month_end]
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        monthly_sales.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(month_revenue)
        })
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_categories': total_categories,
        'total_revenue': total_revenue,
        'today_visits': today_visits,
        'current_online': current_online,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'low_stock_products': low_stock_products,
        'monthly_sales': json.dumps(monthly_sales[::-1]),  # Reverse for chronological order
    }
    
    return render(request, 'custom_admin/dashboard.html', context)

@admin_required
def product_list(request):
    """List all products with search and filtering"""
    
    products = Product.objects.select_related('category').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Stock filter
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'low':
        products = products.filter(stock_quantity__lt=10)
    elif stock_filter == 'out':
        products = products.filter(stock_quantity=0)
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'stock_low':
        products = products.order_by('stock_quantity')
    elif sort_by == 'recent':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'custom_admin/product_list.html', context)

@admin_required
def product_detail(request, product_slug):
    """View and edit product details"""
    
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        # Handle different form actions
        action = request.POST.get('action', 'update_product')
        
        if action == 'update_product':
            # Update product
            product.name = request.POST.get('name', product.name)
            product.description = request.POST.get('description', product.description)
            product.price = float(request.POST.get('price', product.price))
            
            # Handle original price for discount functionality
            original_price = request.POST.get('original_price', '').strip()
            if original_price:
                product.original_price = float(original_price)
            else:
                product.original_price = None
                
            product.stock_quantity = int(request.POST.get('stock', product.stock_quantity))
            product.category_id = request.POST.get('category', product.category_id)
            
            # Handle YouTube URL
            youtube_url = request.POST.get('youtube_url', '').strip()
            product.youtube_url = youtube_url if youtube_url else None
            
            # Handle image upload
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            
        elif action == 'add_images':
            # Handle multiple image uploads
            images = request.FILES.getlist('additional_images')
            if images:
                added_count = 0
                for image in images:
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        alt_text=request.POST.get('alt_text', ''),
                        order=ProductImage.objects.filter(product=product).count()
                    )
                    added_count += 1
                messages.success(request, f'{added_count} image(s) added successfully!')
            else:
                messages.warning(request, 'Please select at least one image to upload.')
        
        return redirect('custom_admin:product_detail', product_slug=product.slug)
    
    categories = Category.objects.all()
    
    # Get order history for this product
    order_items = product.orderitem.select_related('order')[:10]
    
    # Get additional images for this product
    additional_images = product.additional_images.all()
    
    context = {
        'product': product,
        'categories': categories,
        'order_items': order_items,
        'additional_images': additional_images,
    }
    
    return render(request, 'custom_admin/product_detail.html', context)

@admin_required
def product_create(request):
    """Create new product"""
    
    if request.method == 'POST':
        try:
            # Handle original price for discount functionality
            original_price = request.POST.get('original_price', '').strip()
            original_price = float(original_price) if original_price else None
            
            product = Product.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                price=float(request.POST['price']),
                original_price=original_price,
                stock_quantity=int(request.POST['stock']),
                category_id=request.POST['category'],
                image=request.FILES.get('image'),
                youtube_url=request.POST.get('youtube_url', '').strip() or None
            )
            
            # Handle additional images
            additional_images = request.FILES.getlist('additional_images')
            for i, image in enumerate(additional_images):
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    alt_text=request.POST.get('alt_text', ''),
                    order=i
                )
            
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('custom_admin:product_detail', product_slug=product.slug)
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'custom_admin/product_create.html', context)


@admin_required
def product_image_delete(request, image_id):
    """Delete a product image"""
    image = get_object_or_404(ProductImage, id=image_id)
    product_slug = image.product.slug
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
    
    return redirect('custom_admin:product_detail', product_slug=product_slug)


@admin_required
def product_image_reorder(request):
    """Reorder product images via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_orders = data.get('image_orders', [])
            
            for item in image_orders:
                image_id = item.get('id')
                new_order = item.get('order')
                ProductImage.objects.filter(id=image_id).update(order=new_order)
            
            return JsonResponse({'success': True, 'message': 'Images reordered successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@admin_required
def product_delete(request, product_slug):
    """Delete a product immediately"""
    product = get_object_or_404(Product, slug=product_slug)
    product_name = product.name
    
    # Delete the product
    product.delete()
    messages.success(request, f'Product "{product_name}" deleted successfully!')
    return redirect('custom_admin:product_list')

@admin_required
def order_list(request):
    """List all orders with filtering and search"""
    
    orders = Order.objects.prefetch_related('items__product').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_email__icontains=search_query) |
            Q(customer_phone__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Date filter
    date_filter = request.GET.get('date_filter', '')
    if date_filter == 'today':
        orders = orders.filter(created_at__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = timezone.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=month_ago)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    orders = orders.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Order status choices for filter
    status_choices = Order.STATUS_CHOICES if hasattr(Order, 'STATUS_CHOICES') else [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'sort_by': sort_by,
        'status_choices': status_choices,
    }
    
    return render(request, 'custom_admin/order_list.html', context)

@admin_required
def order_detail(request, order_id):
    """View and manage order details"""
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Update order status
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status and hasattr(order, 'status') and new_status != order.status:
            old_status = order.status
            order.status = new_status
            order.save()
            
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                notes=notes or f'Status changed from {dict(Order.STATUS_CHOICES)[old_status]} to {dict(Order.STATUS_CHOICES)[new_status]}',
                created_by=f'Admin ({request.user.username})'
            )
            
            messages.success(request, f'Order status updated to "{dict(Order.STATUS_CHOICES)[new_status]}"')
            return redirect('custom_admin:order_detail', order_id=order.id)
    
    # Get order items and status history
    order_items = order.items.select_related('product')
    status_history = order.status_history.all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'status_history': status_history,
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'custom_admin/order_detail.html', context)

@admin_required
def order_invoice(request, order_id):
    """Generate and display order invoice"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.select_related('product')
    
    # Calculate tax if applicable (you can modify this based on your tax requirements)
    tax_rate = Decimal('0.0')  # Set your tax rate here (e.g., Decimal('0.10') for 10%)
    tax_amount = order.subtotal * tax_rate
    
    context = {
        'order': order,
        'order_items': order_items,
        'tax_rate': tax_rate,
        'tax_amount': tax_amount,
        'invoice_date': timezone.now(),
        'site_settings': SiteSettings.get_current(),
    }
    
    return render(request, 'custom_admin/order_invoice.html', context)

@admin_required
def category_list(request):
    """Manage categories"""
    
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('name')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            try:
                category = Category.objects.create(
                    name=request.POST['name'],
                    description=request.POST.get('description', ''),
                    image=request.FILES.get('image')
                )
                messages.success(request, f'Category "{category.name}" created successfully!')
            except Exception as e:
                messages.error(request, f'Error creating category: {str(e)}')
        
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(id=category_id)
                category_name = category.name
                category.delete()
                messages.success(request, f'Category "{category_name}" deleted successfully!')
            except Category.DoesNotExist:
                messages.error(request, 'Category not found')
            except Exception as e:
                messages.error(request, f'Error deleting category: {str(e)}')
        
        return redirect('custom_admin:category_list')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'custom_admin/category_list.html', context)

@admin_required
def banner_management(request):
    """Manage carousel banners"""
    
    banners = HeroBanner.objects.all().order_by('order')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle':
            banner_id = request.POST.get('banner_id')
            try:
                banner = HeroBanner.objects.get(id=banner_id)
                banner.is_active = not banner.is_active
                banner.save()
                status = 'activated' if banner.is_active else 'deactivated'
                messages.success(request, f'Banner "{banner.title}" {status}!')
            except HeroBanner.DoesNotExist:
                messages.error(request, 'Banner not found')
            except Exception as e:
                messages.error(request, f'Error updating banner: {str(e)}')
        
        return redirect('custom_admin:banner_management')
    
    context = {
        'banners': banners,
    }
    return render(request, 'custom_admin/banner_management.html', context)


@admin_required
def banner_create(request):
    """Create new banner"""
    
    if request.method == 'POST':
        try:
            banner = HeroBanner.objects.create(
                title=request.POST['title'],
                subtitle=request.POST.get('subtitle', ''),
                button_text=request.POST.get('button_text', 'Shop Now'),
                button_url=request.POST.get('button_url', ''),
                order=int(request.POST.get('order', 0)),
                is_active='is_active' in request.POST,
                image=request.FILES.get('image')
            )
            messages.success(request, f'Banner "{banner.title}" created successfully!')
            return redirect('custom_admin:banner_detail', banner_id=banner.id)
        except Exception as e:
            messages.error(request, f'Error creating banner: {str(e)}')
    
    context = {}
    return render(request, 'custom_admin/banner_create.html', context)


@admin_required
def banner_detail(request, banner_id):
    """View and edit banner details"""
    
    banner = get_object_or_404(HeroBanner, id=banner_id)
    
    if request.method == 'POST':
        try:
            # Update banner fields
            banner.title = request.POST.get('title', banner.title)
            banner.subtitle = request.POST.get('subtitle', banner.subtitle)
            banner.button_text = request.POST.get('button_text', banner.button_text)
            banner.button_url = request.POST.get('button_url', banner.button_url)
            banner.order = int(request.POST.get('order', banner.order))
            banner.is_active = 'is_active' in request.POST
            
            # Handle image upload
            if 'image' in request.FILES:
                banner.image = request.FILES['image']
            
            banner.save()
            messages.success(request, f'Banner "{banner.title}" updated successfully!')
            return redirect('custom_admin:banner_detail', banner_id=banner.id)
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
    
    context = {
        'banner': banner,
    }
    return render(request, 'custom_admin/banner_detail.html', context)


@admin_required
def banner_delete(request, banner_id):
    """Delete banner directly"""
    
    banner = get_object_or_404(HeroBanner, id=banner_id)
    banner_title = banner.title
    banner.delete()
    messages.success(request, f'Banner "{banner_title}" deleted successfully!')
    return redirect('custom_admin:banner_management')


@admin_required
def banner_reorder(request):
    """Reorder banners via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            banner_orders = data.get('banner_orders', [])
            
            for item in banner_orders:
                banner_id = item.get('id')
                new_order = item.get('order')
                HeroBanner.objects.filter(id=banner_id).update(order=new_order)
            
            return JsonResponse({'success': True, 'message': 'Banners reordered successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    return render(request, 'custom_admin/banner_management.html', context)

@admin_required
def analytics_view(request):
    """Analytics and reporting"""
    
    # Date range filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    orders = Order.objects.all().order_by('-created_at')  # Order by most recent first
    
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date__lte=date_to)
        except ValueError:
            pass
    
    # Basic metrics
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Best selling products
    best_selling = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity', filter=Q(orderitem__order__in=orders))
    ).order_by('-total_sold')[:10]
    
    # Revenue by category
    category_data = Category.objects.annotate(
        revenue=Sum('products__orderitem__order__total_amount', 
                   filter=Q(products__orderitem__order__in=orders))
    ).order_by('-revenue')
    
    # Calculate percentages
    category_revenue = []
    for category in category_data:
        revenue = category.revenue or 0
        percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
        category_revenue.append({
            'name': category.name,
            'revenue': revenue,
            'percentage': percentage
        })
    
    # Daily sales for chart
    daily_sales = []
    if date_from and date_to:
        current_date = date_from
        while current_date <= date_to:
            day_revenue = orders.filter(
                created_at__date=current_date
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            daily_sales.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'revenue': float(day_revenue)
            })
            current_date += timedelta(days=1)
    
    # User visit statistics
    today = timezone.now().date()
    
    # Today's visits
    today_visits = UserVisit.objects.filter(date=today).count()
    
    # Yesterday's visits for comparison
    yesterday = today - timedelta(days=1)
    yesterday_visits = UserVisit.objects.filter(date=yesterday).count()
    
    # Calculate percentage change
    visit_change = today_visits - yesterday_visits
    if yesterday_visits > 0:
        visit_change_percent = (visit_change / yesterday_visits) * 100
    else:
        visit_change_percent = 0 if visit_change == 0 else 100
    
    # Current online users (active in last 5 minutes)
    current_online = OnlineUser.objects.count()
    
    # Total visits this month
    month_start = today.replace(day=1)
    month_visits = UserVisit.objects.filter(date__gte=month_start).count()
    
    # Daily visits for the past 7 days
    daily_visits = []
    for i in range(6, -1, -1):
        check_date = today - timedelta(days=i)
        visits_count = UserVisit.objects.filter(date=check_date).count()
        daily_visits.append({
            'date': check_date.strftime('%Y-%m-%d'),
            'visits': visits_count
        })
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'average_order_value': average_order_value,
        'best_selling': best_selling,
        'category_revenue': category_revenue,
        'daily_sales': json.dumps(daily_sales),
        'date_from': date_from.strftime('%Y-%m-%d') if date_from else '',
        'date_to': date_to.strftime('%Y-%m-%d') if date_to else '',
        # Visit statistics
        'today_visits': today_visits,
        'yesterday_visits': yesterday_visits,
        'visit_change': visit_change,
        'visit_change_percent': visit_change_percent,
        'current_online': current_online,
        'month_visits': month_visits,
        'daily_visits': json.dumps(daily_visits),
    }
    
    return render(request, 'custom_admin/analytics.html', context)

@admin_required
def settings_view(request):
    """Admin settings and configuration"""
    
    # Get current site settings
    branding = SiteSettings.get_current()
    
    # Default general settings
    default_settings = {
        'admin_email': 'admin@example.com',
        'items_per_page': 25,
    }
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'branding':
            # Handle branding form
            try:
                branding.site_name = request.POST.get('site_name', branding.site_name)
                branding.site_tagline = request.POST.get('site_tagline', '')
                branding.header_bg_color = request.POST.get('header_bg_color', branding.header_bg_color)
                branding.header_text_color = request.POST.get('header_text_color', branding.header_text_color)
                branding.phone_number = request.POST.get('phone_number', '')
                branding.email = request.POST.get('email', '')
                branding.address = request.POST.get('address', '')
                branding.facebook_url = request.POST.get('facebook_url', '')
                branding.youtube_url = request.POST.get('youtube_url', '')
                branding.meta_description = request.POST.get('meta_description', '')
                branding.meta_keywords = request.POST.get('meta_keywords', '')
                
                # Handle file uploads
                if 'logo' in request.FILES:
                    branding.logo = request.FILES['logo']
                if 'favicon' in request.FILES:
                    branding.favicon = request.FILES['favicon']
                
                branding.save()
                messages.success(request, 'Site branding updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating branding: {str(e)}')
                
        elif form_type == 'general':
            # Handle general settings form
            admin_email = request.POST.get('admin_email', default_settings['admin_email'])
            items_per_page = int(request.POST.get('items_per_page', default_settings['items_per_page']))
            
            # Save to session for persistence
            request.session['admin_settings'] = {
                'admin_email': admin_email,
                'items_per_page': items_per_page,
            }
            
            messages.success(request, 'General settings updated successfully!')
        
        return redirect('custom_admin:settings')
    
    # Get general settings from session or use defaults
    saved_settings = request.session.get('admin_settings', default_settings)
    
    # Get database name
    from django.conf import settings as django_settings
    import os
    db_settings = django_settings.DATABASES.get('default', {})
    db_engine = db_settings.get('ENGINE', '')
    db_name = db_settings.get('NAME', '')
    if 'sqlite' in db_engine and db_name:
        database_name = os.path.basename(db_name)
    else:
        database_name = db_name or 'Unknown'

    import shutil
    try:
        usage = shutil.disk_usage("/")
        total_storage = f"{usage.total // (1024 * 1024 * 1024)} GB"
        available_storage = f"{usage.free // (1024 * 1024 * 1024)} GB"
    except Exception:
        total_storage = "Unknown"
        available_storage = "Unknown"

    context = {
        'branding': branding,
        'admin_email': saved_settings.get('admin_email', default_settings['admin_email']),
        'items_per_page': saved_settings.get('items_per_page', default_settings['items_per_page']),
        'database_name': database_name,
        'total_storage': total_storage,
        'available_storage': available_storage,
    }
    return render(request, 'custom_admin/settings.html', context)


@admin_required
def featured_products(request):
    """Manage featured products and best sellers"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            
            if action == 'toggle_featured':
                product.is_featured = not product.is_featured
                product.save()
                status = 'featured' if product.is_featured else 'not featured'
                messages.success(request, f'"{product.name}" is now {status}.')
                
            elif action == 'toggle_bestseller':
                product.is_best_seller = not product.is_best_seller
                product.save()
                status = 'a best seller' if product.is_best_seller else 'not a best seller'
                messages.success(request, f'"{product.name}" is now {status}.')
                
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
        
        return redirect('custom_admin:featured_products')
    
    # Get all products with their status
    products = Product.objects.all().order_by('name')
    featured_products = Product.objects.filter(is_featured=True)
    best_sellers = Product.objects.filter(is_best_seller=True)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'featured_products': featured_products,
        'best_sellers': best_sellers,
        'featured_count': featured_products.count(),
        'bestseller_count': best_sellers.count(),
    }
    
    return render(request, 'custom_admin/featured_products.html', context)

# AJAX Views
@admin_required
@require_http_methods(["POST"])
def quick_status_update(request):
    """Quick AJAX status update for orders"""
    try:
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        order = Order.objects.get(id=order_id)
        if hasattr(order, 'status'):
            order.status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Order status updated to {new_status}'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Order model does not have status field'
            })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


def admin_login(request):
    """Custom admin login view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    next_url = request.GET.get('next', 'custom_admin:dashboard')
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    return redirect(next_url)
                else:
                    messages.error(request, 'You do not have permission to access the admin panel.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')
    
    return render(request, 'custom_admin/login.html')


def admin_logout(request):
    """Custom admin logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('custom_admin:login')


@admin_required
def admin_profile(request):
    """Admin profile management view"""
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        
        # Update basic info
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        
        # Handle password change if provided
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password:
            if not current_password:
                messages.error(request, 'Current password is required to change password.')
            elif not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            else:
                user.set_password(new_password)
                messages.success(request, 'Password updated successfully. Please log in again.')
                user.save()
                logout(request)
                return redirect('custom_admin:login')
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('custom_admin:profile')
    
    return render(request, 'custom_admin/profile.html', {
        'user': request.user,
        'title': 'Admin Profile'
    })

# Category Management Views

@admin_required
def category_list(request):
    """List all categories with hierarchical structure and search functionality"""
    
    # Get root categories first
    categories = Category.objects.filter(parent=None).prefetch_related('children').order_by('name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        categories = Category.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        ).order_by('name')
    
    # If searching, show all matching categories (not just root)
    if not search_query:
        # For non-search view, build hierarchical structure
        def build_category_tree(categories):
            tree = []
            for category in categories:
                tree.append({
                    'category': category,
                    'children': build_category_tree(category.children.order_by('name'))
                })
            return tree
        
        category_tree = build_category_tree(categories)
    else:
        category_tree = None
    
    # Pagination
    paginator = Paginator(categories, 20)
    page_number = request.GET.get('page')
    categories_page = paginator.get_page(page_number)
    
    context = {
        'categories': categories_page,
        'category_tree': category_tree,
        'search_query': search_query,
        'total_categories': Category.objects.count(),
        'root_categories_count': Category.objects.filter(parent=None).count(),
    }
    
    return render(request, 'custom_admin/category_list.html', context)

@admin_required
def category_detail(request, category_slug):
    """View and edit category details with parent/child relationships"""
    
    category = get_object_or_404(Category, slug=category_slug)
    
    if request.method == 'POST':
        # Update category
        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', category.description)
        
        # Handle parent category
        parent_id = request.POST.get('parent')
        if parent_id:
            try:
                parent_category = Category.objects.get(id=parent_id)
                # Prevent circular reference
                if not parent_category.is_child_of(category) and parent_category != category:
                    category.parent = parent_category
                else:
                    messages.error(request, 'Cannot set parent: This would create a circular reference!')
                    return redirect('custom_admin:category_detail', category_slug=category.slug)
            except Category.DoesNotExist:
                messages.error(request, 'Selected parent category does not exist!')
                return redirect('custom_admin:category_detail', category_slug=category.slug)
        else:
            category.parent = None
        
        # Handle image upload
        if 'image' in request.FILES:
            category.image = request.FILES['image']
        
        try:
            category.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('custom_admin:category_detail', category_slug=category.slug)
        except Exception as e:
            messages.error(request, f'Error updating category: {str(e)}')
    
    # Get products in this category and subcategories
    products = category.products.all()[:10]
    product_count = category.products.count()
    
    # Get subcategory products count
    subcategory_product_count = 0
    for child in category.get_all_children():
        subcategory_product_count += child.products.count()
    
    # Get possible parent categories (exclude self and its children)
    excluded_ids = [category.id] + [child.id for child in category.get_all_children()]
    possible_parents = Category.objects.exclude(id__in=excluded_ids).order_by('name')
    
    context = {
        'category': category,
        'products': products,
        'product_count': product_count,
        'subcategory_product_count': subcategory_product_count,
        'possible_parents': possible_parents,
        'children': category.children.all(),
        'full_path': category.full_path,
        'level': category.get_level(),
    }
    
    return render(request, 'custom_admin/category_detail.html', context)

@admin_required
def category_create(request):
    """Create new category with optional parent"""
    
    if request.method == 'POST':
        try:
            parent = None
            parent_id = request.POST.get('parent')
            if parent_id:
                parent = Category.objects.get(id=parent_id)
            
            category = Category.objects.create(
                name=request.POST['name'],
                description=request.POST.get('description', ''),
                image=request.FILES.get('image'),
                parent=parent
            )
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('custom_admin:category_detail', category_slug=category.slug)
        except Exception as e:
            messages.error(request, f'Error creating category: {str(e)}')
    
    # Get all categories for parent selection
    categories = Category.objects.all().order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'custom_admin/category_create.html', context)

@admin_required
def category_delete(request, category_slug):
    """Delete a category with hierarchy check"""
    category = get_object_or_404(Category, slug=category_slug)
    
    # Check if category has products
    product_count = category.products.count()
    
    # Check if category has children
    children_count = category.children.count()
    
    if product_count > 0:
        messages.error(request, f'Cannot delete category "{category.name}" because it contains {product_count} products. Please move or delete the products first.')
        return redirect('custom_admin:category_detail', category_slug=category.slug)
    
    if children_count > 0:
        messages.error(request, f'Cannot delete category "{category.name}" because it has {children_count} subcategories. Please move or delete the subcategories first.')
        return redirect('custom_admin:category_detail', category_slug=category.slug)
    
    # Delete the category directly
    category_name = category.name
    category.delete()
    messages.success(request, f'Category "{category_name}" deleted successfully!')
    return redirect('custom_admin:category_list')
