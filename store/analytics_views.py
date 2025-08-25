from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Product, Order, OrderItem, Category
import json

@staff_member_required
def analytics_dashboard(request):
    """Analytics dashboard for admin users"""
    
    # Basic Stats
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Active products (in stock)
    active_products = Product.objects.filter(stock_quantity__gt=0).count()
    
    # Recent orders (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago).count()
    recent_revenue = Order.objects.filter(
        created_at__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Order status breakdown
    order_status_stats = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Top selling products
    top_products = OrderItem.objects.values(
        'product__name', 'product__id'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('quantity') * Sum('price')
    ).order_by('-total_sold')[:10]
    
    # Category performance
    category_stats = Category.objects.annotate(
        product_count=Count('products'),
        total_sold=Sum('products__orderitem__quantity'),
        revenue=Sum('products__orderitem__quantity') * Sum('products__orderitem__price')
    ).order_by('-total_sold')[:10]
    
    # Monthly revenue trend (last 12 months)
    monthly_revenue = []
    for i in range(12):
        month_start = (timezone.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        revenue = Order.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        monthly_revenue.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(revenue)
        })
    
    monthly_revenue.reverse()  # Show oldest to newest
    
    # Low stock alerts
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=10,
        stock_quantity__gt=0
    ).order_by('stock_quantity')[:10]
    
    # Out of stock products
    out_of_stock_products = Product.objects.filter(
        stock_quantity=0
    ).count()
    
    # Average order value
    avg_order_value = Order.objects.aggregate(
        avg=Sum('total_amount') / Count('id')
    )['avg'] or 0
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_revenue': recent_revenue,
        'order_status_stats': order_status_stats,
        'top_products': top_products,
        'category_stats': category_stats,
        'monthly_revenue': monthly_revenue,
        'monthly_revenue_json': json.dumps(monthly_revenue),
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'avg_order_value': avg_order_value,
    }
    
    return render(request, 'admin/analytics_dashboard.html', context)

@staff_member_required
def product_analytics(request):
    """Detailed product analytics"""
    
    # Best selling products
    best_sellers = OrderItem.objects.values(
        'product__name', 'product__id', 'product__price', 'product__stock_quantity'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum('quantity') * Sum('price')
    ).order_by('-total_sold')[:20]
    
    # Low performing products (least sold)
    low_performers = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(
        total_sold__isnull=True
    ).order_by('-created_at')[:10]  # Products never sold
    
    # Category breakdown
    category_performance = Category.objects.annotate(
        product_count=Count('products'),
        total_sold=Sum('products__orderitem__quantity'),
        revenue=Sum('products__orderitem__quantity') * Sum('products__orderitem__price')
    ).order_by('-revenue')
    
    context = {
        'best_sellers': best_sellers,
        'low_performers': low_performers,
        'category_performance': category_performance,
    }
    
    return render(request, 'admin/product_analytics.html', context)

@staff_member_required
def order_analytics(request):
    """Detailed order analytics"""
    
    # Daily orders trend (last 30 days)
    daily_orders = []
    for i in range(30):
        date = timezone.now().date() - timedelta(days=i)
        orders_count = Order.objects.filter(created_at__date=date).count()
        revenue = Order.objects.filter(
            created_at__date=date
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        daily_orders.append({
            'date': date.strftime('%Y-%m-%d'),
            'orders': orders_count,
            'revenue': float(revenue)
        })
    
    daily_orders.reverse()  # Show oldest to newest
    
    # Order status distribution
    status_distribution = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Average order processing time (for completed orders)
    completed_orders = Order.objects.filter(
        status__in=['delivered', 'shipped']
    ).values('created_at', 'updated_at')
    
    # Payment method stats
    payment_stats = Order.objects.values('payment_method').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    ).order_by('-count')
    
    context = {
        'daily_orders': daily_orders,
        'daily_orders_json': json.dumps(daily_orders),
        'status_distribution': status_distribution,
        'payment_stats': payment_stats,
    }
    
    return render(request, 'admin/order_analytics.html', context)
