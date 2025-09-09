from .models import CartItem, Category, SiteSettings

def site_settings(request):
    """Add site settings to all templates"""
    site_settings = SiteSettings.get_current()
    return {
        'site_settings': site_settings,
        'site_name': site_settings.site_name,
        'site_tagline': site_settings.site_tagline,
    }

def cart_count(request):
    """Add cart count and categories to all templates"""
    if not request.session.session_key:
        request.session.create()
    
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    
    # Add categories for navigation
    categories = Category.objects.all()
    
    return {
        'cart_count': total_items,
        'cart_total': total_price,
        'categories': categories,
    }
