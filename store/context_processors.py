def site_settings(request):
    site_settings = SiteSettings.get_current()
    return {
        'site_settings': site_settings,
        'site_name': site_settings.site_name,
        'site_tagline': site_settings.site_tagline,
    }
from .models import CartItem, Category, SiteSettings

def cart_count(request):
    """Add cart count and hierarchical categories to all templates"""
    if not request.session.session_key:
        request.session.create()
    
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    
    # Add hierarchical categories for navigation
    categories = Category.objects.all()
    root_categories = Category.get_root_categories().prefetch_related('children__children')
    
    # Build hierarchical category structure for menu
    def build_category_menu(categories):
        menu_items = []
        for category in categories:
            menu_items.append({
                'category': category,
                'children': build_category_menu(category.children.all()) if category.children.exists() else []
            })
        return menu_items
    
    category_menu = build_category_menu(root_categories)
    
    # Add site settings for branding
    site_settings = SiteSettings.get_current()
    
    return {
        'cart_count': total_items,
        'cart_total': total_price,
        'categories': categories,
        'root_categories': root_categories,
        'category_menu': category_menu,
        'site_settings': site_settings,
        'site_name': site_settings.site_name,
        'site_tagline': site_settings.site_tagline,
    }
