from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product, Category, HeroBanner
from PIL import Image, ImageDraw, ImageFont
import io
import os

class Command(BaseCommand):
    help = 'Create placeholder images for products'

    def create_placeholder_image(self, text, width=400, height=400, color='#f0f0f0'):
        """Create a simple placeholder image with text"""
        # Create image
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, fill='#666666', font=font)
        
        # Add a simple border
        draw.rectangle([0, 0, width-1, height-1], outline='#cccccc', width=2)
        
        return img

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating placeholder images...'))
        
        # Color scheme for different categories
        category_colors = {
            'Electronics': '#e3f2fd',
            'Clothing': '#fce4ec',
            'Home & Garden': '#e8f5e8',
            'Sports & Outdoors': '#fff3e0',
            'Books': '#f3e5f5',
            'Health & Beauty': '#e0f2f1'
        }
        
        # Create placeholder images for products
        products_without_images = Product.objects.filter(image='')
        
        for product in products_without_images:
            try:
                # Get category color or default
                color = category_colors.get(product.category.name, '#f0f0f0')
                
                # Create placeholder image
                img = self.create_placeholder_image(
                    product.name[:20] + '...' if len(product.name) > 20 else product.name,
                    color=color
                )
                
                # Save to BytesIO
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)
                
                # Create filename
                filename = f"{product.name.lower().replace(' ', '_').replace('&', 'and')[:30]}.jpg"
                
                # Save to product
                product.image.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(f'Created image for: {product.name}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to create image for {product.name}: {str(e)}')
                )
        
        # Create placeholder images for categories
        categories_without_images = Category.objects.filter(image='')
        
        for category in categories_without_images:
            try:
                color = category_colors.get(category.name, '#f0f0f0')
                
                # Create smaller image for categories
                img = self.create_placeholder_image(
                    category.name,
                    width=200,
                    height=200,
                    color=color
                )
                
                # Save to BytesIO
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)
                
                # Create filename
                filename = f"category_{category.name.lower().replace(' ', '_').replace('&', 'and')}.jpg"
                
                # Save to category
                category.image.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(f'Created image for category: {category.name}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to create image for category {category.name}: {str(e)}')
                )
        
        # Create hero banner images
        banners_without_images = HeroBanner.objects.filter(image='')
        banner_colors = ['#4f46e5', '#059669', '#dc2626']
        
        for i, banner in enumerate(banners_without_images):
            try:
                color = banner_colors[i % len(banner_colors)]
                
                # Create banner image
                img = self.create_placeholder_image(
                    banner.title,
                    width=1200,
                    height=400,
                    color=color
                )
                
                # Save to BytesIO
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)
                
                # Create filename
                filename = f"banner_{banner.title.lower().replace(' ', '_')[:20]}.jpg"
                
                # Save to banner
                banner.image.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(f'Created image for banner: {banner.title}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to create image for banner {banner.title}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Placeholder images created successfully!\n'
                'Your e-commerce site is now ready with sample products and images.'
            )
        )
