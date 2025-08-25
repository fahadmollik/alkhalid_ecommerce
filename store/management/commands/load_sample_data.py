from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Category, Product, HeroBanner
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load sample data for the e-commerce store'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))
        
        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronic gadgets and devices'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for all occasions'
            },
            {
                'name': 'Home & Garden',
                'description': 'Everything for your home and garden'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment and outdoor gear'
            },
            {
                'name': 'Books',
                'description': 'Books and educational materials'
            },
            {
                'name': 'Health & Beauty',
                'description': 'Health and beauty products'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
                'price': 89.99,
                'category': 'Electronics',
                'stock_quantity': 50,
                'is_best_seller': True,
                'is_featured': True
            },
            {
                'name': 'Smartphone Stand',
                'description': 'Adjustable smartphone stand made from premium aluminum. Compatible with all phone sizes and tablets.',
                'price': 24.99,
                'category': 'Electronics',
                'stock_quantity': 100,
                'is_best_seller': False,
                'is_featured': False
            },
            {
                'name': '4K Webcam',
                'description': 'Ultra HD 4K webcam with auto-focus and built-in microphone. Perfect for streaming and video calls.',
                'price': 129.99,
                'category': 'Electronics',
                'stock_quantity': 30,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Wireless Charging Pad',
                'description': 'Fast wireless charging pad compatible with all Qi-enabled devices. Sleek design with LED indicators.',
                'price': 34.99,
                'category': 'Electronics',
                'stock_quantity': 75,
                'is_best_seller': False,
                'is_featured': True
            },
            
            # Clothing
            {
                'name': 'Classic Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors. Pre-shrunk and machine washable.',
                'price': 19.99,
                'category': 'Clothing',
                'stock_quantity': 200,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Denim Jacket',
                'description': 'Stylish denim jacket made from premium cotton denim. Classic fit with vintage wash.',
                'price': 79.99,
                'category': 'Clothing',
                'stock_quantity': 45,
                'is_best_seller': False,
                'is_featured': True
            },
            {
                'name': 'Running Shoes',
                'description': 'Lightweight running shoes with advanced cushioning technology. Breathable mesh upper.',
                'price': 119.99,
                'category': 'Clothing',
                'stock_quantity': 60,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Winter Wool Scarf',
                'description': 'Soft merino wool scarf perfect for cold weather. Available in various colors and patterns.',
                'price': 39.99,
                'category': 'Clothing',
                'stock_quantity': 80,
                'is_best_seller': False,
                'is_featured': False
            },
            
            # Home & Garden
            {
                'name': 'LED Desk Lamp',
                'description': 'Adjustable LED desk lamp with multiple brightness levels and USB charging port. Eye-care technology.',
                'price': 49.99,
                'category': 'Home & Garden',
                'stock_quantity': 40,
                'is_best_seller': False,
                'is_featured': True
            },
            {
                'name': 'Indoor Plant Pot Set',
                'description': 'Set of 3 ceramic plant pots with drainage holes and saucers. Perfect for indoor plants.',
                'price': 29.99,
                'category': 'Home & Garden',
                'stock_quantity': 90,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Memory Foam Pillow',
                'description': 'Ergonomic memory foam pillow with cooling gel layer. Hypoallergenic and machine washable cover.',
                'price': 59.99,
                'category': 'Home & Garden',
                'stock_quantity': 35,
                'is_best_seller': False,
                'is_featured': False
            },
            {
                'name': 'Kitchen Knife Set',
                'description': 'Professional 8-piece kitchen knife set with wooden block. High-carbon stainless steel blades.',
                'price': 149.99,
                'category': 'Home & Garden',
                'stock_quantity': 25,
                'is_best_seller': True,
                'is_featured': True
            },
            
            # Sports & Outdoors
            {
                'name': 'Yoga Mat',
                'description': 'Non-slip yoga mat made from eco-friendly TPE material. Extra thick for comfort and support.',
                'price': 34.99,
                'category': 'Sports & Outdoors',
                'stock_quantity': 70,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Water Bottle',
                'description': 'Insulated stainless steel water bottle keeps drinks cold for 24 hours or hot for 12 hours.',
                'price': 24.99,
                'category': 'Sports & Outdoors',
                'stock_quantity': 120,
                'is_best_seller': False,
                'is_featured': False
            },
            {
                'name': 'Camping Backpack',
                'description': '50L hiking backpack with multiple compartments and rain cover. Perfect for weekend trips.',
                'price': 89.99,
                'category': 'Sports & Outdoors',
                'stock_quantity': 30,
                'is_best_seller': False,
                'is_featured': True
            },
            
            # Books
            {
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming for beginners and intermediate developers.',
                'price': 39.99,
                'category': 'Books',
                'stock_quantity': 50,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Web Development Handbook',
                'description': 'Complete handbook covering HTML, CSS, JavaScript, and modern web frameworks.',
                'price': 44.99,
                'category': 'Books',
                'stock_quantity': 40,
                'is_best_seller': False,
                'is_featured': True
            },
            {
                'name': 'Digital Marketing Essentials',
                'description': 'Learn the fundamentals of digital marketing, SEO, and social media marketing.',
                'price': 34.99,
                'category': 'Books',
                'stock_quantity': 60,
                'is_best_seller': False,
                'is_featured': False
            },
            
            # Health & Beauty
            {
                'name': 'Vitamin C Serum',
                'description': 'Anti-aging vitamin C serum with hyaluronic acid. Brightens skin and reduces fine lines.',
                'price': 29.99,
                'category': 'Health & Beauty',
                'stock_quantity': 80,
                'is_best_seller': True,
                'is_featured': False
            },
            {
                'name': 'Electric Toothbrush',
                'description': 'Rechargeable electric toothbrush with multiple cleaning modes and timer function.',
                'price': 79.99,
                'category': 'Health & Beauty',
                'stock_quantity': 40,
                'is_best_seller': False,
                'is_featured': True
            },
            {
                'name': 'Essential Oil Diffuser',
                'description': 'Ultrasonic essential oil diffuser with color-changing LED lights and auto shut-off.',
                'price': 49.99,
                'category': 'Health & Beauty',
                'stock_quantity': 55,
                'is_best_seller': False,
                'is_featured': False
            }
        ]

        # Create products
        for product_data in products_data:
            category = categories[product_data['category']]
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': category,
                    'stock_quantity': product_data['stock_quantity'],
                    'is_best_seller': product_data['is_best_seller'],
                    'is_featured': product_data['is_featured']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create hero banners
        hero_banners_data = [
            {
                'title': 'Summer Sale - Up to 50% Off!',
                'subtitle': 'Discover amazing deals on electronics, clothing, and more',
                'button_text': 'Shop Now',
                'is_active': True,
                'order': 1
            },
            {
                'title': 'New Arrivals',
                'subtitle': 'Check out our latest products and trending items',
                'button_text': 'Explore',
                'is_active': True,
                'order': 2
            },
            {
                'title': 'Free Shipping',
                'subtitle': 'Free delivery on all orders over $50',
                'button_text': 'Learn More',
                'is_active': True,
                'order': 3
            }
        ]

        for banner_data in hero_banners_data:
            banner, created = HeroBanner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            if created:
                self.stdout.write(f'Created hero banner: {banner.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded sample data!\n'
                f'- Categories: {Category.objects.count()}\n'
                f'- Products: {Product.objects.count()}\n'
                f'- Hero Banners: {HeroBanner.objects.count()}\n\n'
                f'Note: Product images are not included in this sample data.\n'
                f'You can add images through the admin panel at /admin/'
            )
        )
