from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, HeroBanner, CartItem, Order, OrderItem, DeliveryOption, OrderStatusHistory
import json

def home(request):
    """Home page with hero banners, categories, and featured products"""
    hero_banners = HeroBanner.objects.filter(is_active=True)
    categories = Category.objects.all()  # Get all categories for carousel
    best_sellers = Product.objects.filter(is_best_seller=True, stock_quantity__gt=0)[:8]
    featured_products = Product.objects.filter(is_featured=True, stock_quantity__gt=0)[:4]  # Bring back featured products
    all_products = Product.objects.filter(stock_quantity__gt=0)[:12]  # Keep all products section
    
    # Get cart product ids for current session
    cart_product_ids = []
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_product_ids = list(cart_items.values_list('product_id', flat=True))
    context = {
        'hero_banners': hero_banners,
        'categories': categories,
        'best_sellers': best_sellers,
        'featured_products': featured_products,
        'all_products': all_products,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'store/home.html', context)

def products(request):
    """All products page with pagination and filtering"""
    product_list = Product.objects.filter(stock_quantity__gt=0)
    category_id = request.GET.get('category')
    search = request.GET.get('search')
    featured = request.GET.get('featured')
    current_category_obj = None
    
    if category_id:
        try:
            current_category_obj = Category.objects.get(id=category_id)
            product_list = product_list.filter(category_id=category_id)
        except Category.DoesNotExist:
            pass
    
    if search:
        product_list = product_list.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    
    if featured:
        product_list = product_list.filter(is_best_seller=True)
    
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    # Get cart product ids for current session
    cart_product_ids = []
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_product_ids = list(cart_items.values_list('product_id', flat=True))
    context = {
        'products': products_page,
        'categories': categories,
        'current_category': category_id,
        'current_category_obj': current_category_obj,
        'search_query': search,
        'featured': featured,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'store/products.html', context)

def category_products(request, category_slug):
    """Products by category"""
    category = get_object_or_404(Category, slug=category_slug)
    product_list = Product.objects.filter(category=category, stock_quantity__gt=0)
    
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    # Get cart product ids for current session
    cart_product_ids = []
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_product_ids = list(cart_items.values_list('product_id', flat=True))
    context = {
        'category': category,
        'products': products_page,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'store/category_products.html', context)

def product_detail(request, product_slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=product_slug)
    related_products = Product.objects.filter(
        category=product.category, 
        stock_quantity__gt=0
    ).exclude(id=product.id)[:4]
    
    # Get cart product ids for current session
    cart_product_ids = []
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_product_ids = list(cart_items.values_list('product_id', flat=True))
    context = {
        'product': product,
        'related_products': related_products,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'store/product_detail.html', context)

def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        if not request.session.session_key:
            request.session.create()
        
        quantity = int(request.POST.get('quantity', 1))
        
        # Debug: Print what we're receiving
        print(f"=== ADD TO CART DEBUG ===")
        print(f"Product: {product.name}")
        print(f"Requested quantity: {quantity}")
        print(f"POST data: {dict(request.POST)}")
        print(f"Session key: {request.session.session_key}")
        
        if quantity > product.stock_quantity:
            messages.error(request, 'Not enough stock available.')
            return redirect('product_detail', product_id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            session_key=request.session.session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            print(f"Existing cart item found - current quantity: {cart_item.quantity}")
            new_quantity = cart_item.quantity + quantity
            print(f"New quantity will be: {new_quantity}")
            if new_quantity > product.stock_quantity:
                messages.error(request, 'Not enough stock available.')
                return redirect('product_detail', product_id=product_id)
            cart_item.quantity = new_quantity
            cart_item.save()
            print(f"Updated cart item quantity to: {cart_item.quantity}")
        else:
            print(f"Created new cart item with quantity: {cart_item.quantity}")
        
        # Debug: Check all cart items for this session
        all_cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        print(f"All cart items for session:")
        for item in all_cart_items:
            print(f"  - {item.product.name}: quantity {item.quantity}")
        print("=== END DEBUG ===")
        
        messages.success(request, f'{product.name} added to cart!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Product added to cart!'})
        
        return redirect('cart')
    
    return redirect('home')

def cart(request):
    """Shopping cart page"""
    if not request.session.session_key:
        request.session.create()
    
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    total = sum(item.total_price for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'total_quantity': total_quantity,
    }
    return render(request, 'store/cart.html', context)

def update_cart(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            import json
            try:
                data = json.loads(request.body)
                quantity = int(data.get('quantity', 1))
            except (json.JSONDecodeError, ValueError):
                return JsonResponse({'success': False, 'message': 'Invalid data'})
        else:
            quantity = int(request.POST.get('quantity', 1))
        
        if quantity > cart_item.product.stock_quantity:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Not enough stock available.'})
            messages.error(request, 'Not enough stock available.')
        elif quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Calculate new totals
                cart_items = CartItem.objects.filter(session_key=request.session.session_key)
                cart_total = sum(item.total_price for item in cart_items)
                total_quantity = sum(item.quantity for item in cart_items)
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Cart updated!',
                    'item_total': float(cart_item.total_price),
                    'cart_total': float(cart_total),
                    'total_quantity': total_quantity,
                    'item_quantity': cart_item.quantity
                })
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                cart_items = CartItem.objects.filter(session_key=request.session.session_key)
                cart_total = sum(item.total_price for item in cart_items)
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Item removed from cart!',
                    'cart_total': float(cart_total),
                    'cart_empty': not cart_items.exists()
                })
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Calculate new totals for AJAX response
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.total_price for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True, 
            'message': 'Item removed from cart!',
            'cart_total': float(cart_total),
            'total_quantity': total_quantity,
            'cart_empty': not cart_items.exists()
        })
    
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

def checkout(request):
    """Checkout page"""
    if not request.session.session_key:
        request.session.create()
    
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    delivery_options = DeliveryOption.objects.filter(is_active=True)
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    subtotal = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Get delivery option
        delivery_option_id = request.POST.get('delivery_option')
        delivery_option = None
        delivery_fee = 0
        
        if delivery_option_id:
            try:
                delivery_option = DeliveryOption.objects.get(id=delivery_option_id, is_active=True)
                delivery_fee = delivery_option.price
            except DeliveryOption.DoesNotExist:
                messages.error(request, 'Invalid delivery option selected!')
                return redirect('checkout')
        
        total_amount = subtotal + delivery_fee
        
        # Create order
        order = Order.objects.create(
            customer_name=request.POST.get('customer_name'),
            customer_email=request.POST.get('customer_email', ''),
            customer_phone=request.POST.get('customer_phone'),
            shipping_address=request.POST.get('shipping_address'),
            delivery_option=delivery_option,
            delivery_fee=delivery_fee,
            subtotal=subtotal,
            total_amount=total_amount,
            notes=request.POST.get('notes', '')
        )
        
        # Create initial status history entry
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Order placed successfully via website',
            created_by='Customer'
        )
        
        # Create order items and update stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            cart_item.product.stock_quantity -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order {order.order_id} placed successfully! Your tracking number is: {order.tracking_number}')
        return redirect('order_confirmation', order_id=order.order_id)
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_options': delivery_options,
    }
    return render(request, 'store/checkout.html', context)

def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, order_id=order_id)
    context = {'order': order}
    return render(request, 'store/order_confirmation.html', context)

def track_order(request):
    """Order tracking page"""
    order = None
    error_message = None
    
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number', '').strip()
        if tracking_number:
            try:
                order = Order.objects.get(
                    Q(tracking_number=tracking_number) | Q(order_id=tracking_number)
                )
            except Order.DoesNotExist:
                error_message = "Order not found. Please check your tracking number and try again."
        else:
            error_message = "Please enter a tracking number."
    
    context = {
        'order': order,
        'error_message': error_message,
    }
    return render(request, 'store/track_order.html', context)

def order_tracking_details(request, tracking_number):
    """Detailed tracking page for a specific order"""
    order = get_object_or_404(Order, 
        Q(tracking_number=tracking_number) | Q(order_id=tracking_number)
    )
    
    # Get status history
    status_history = order.status_history.all()
    
    # Define tracking timeline with all possible statuses
    timeline_statuses = [
        'pending', 'confirmed', 'processing', 'shipped', 'out_for_delivery', 'delivered'
    ]
    
    # Build timeline with completion status
    timeline = []
    for status in timeline_statuses:
        status_info = {
            'status': status,
            'display': dict(Order.STATUS_CHOICES)[status],
            'completed': False,
            'current': False,
            'icon': {
                'pending': 'bi-clock',
                'confirmed': 'bi-check-circle',
                'processing': 'bi-gear',
                'shipped': 'bi-truck',
                'out_for_delivery': 'bi-geo-alt',
                'delivered': 'bi-check-circle-fill',
            }.get(status, 'bi-circle'),
            'date': None,
        }
        
        # Check if this status has been reached
        current_status_index = timeline_statuses.index(order.status) if order.status in timeline_statuses else -1
        status_index = timeline_statuses.index(status)
        
        if status_index <= current_status_index:
            status_info['completed'] = True
            
        if status == order.status:
            status_info['current'] = True
            
        # Get the date from status history if available
        history_entry = status_history.filter(status=status).first()
        if history_entry:
            status_info['date'] = history_entry.created_at
            
        timeline.append(status_info)
    
    context = {
        'order': order,
        'timeline': timeline,
        'status_history': status_history,
    }
    return render(request, 'store/order_tracking_details.html', context)

def contact(request):
    """Contact page"""
    return render(request, 'store/contact.html')

def about(request):
    """About Us page"""
    return render(request, 'store/about.html')

def return_refund(request):
    """Return & Refund Policy page"""
    return render(request, 'store/return-refund.html')

def terms_conditions(request):
    """Terms & Conditions page"""
    return render(request, 'store/terms-conditions.html')

def cookie_policy(request):
    """Cookie Policy page"""
    return render(request, 'store/cookie-policy.html')

def privacy_policy(request):
    """Privacy Policy page"""
    return render(request, 'store/privacy-policy.html')

def buy_now(request, product_id):
    """Adds product to cart and redirects to checkout for direct purchase."""
    product = get_object_or_404(Product, id=product_id)
    # Optionally clear cart for direct buy
    if not request.session.session_key:
        request.session.create()
    cart_item, created = CartItem.objects.get_or_create(
        session_key=request.session.session_key,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity = 1
        cart_item.save()
    # Optionally clear other cart items for true 'Buy Now' experience
    CartItem.objects.filter(session_key=request.session.session_key).exclude(product=product).delete()
    return redirect('checkout')
