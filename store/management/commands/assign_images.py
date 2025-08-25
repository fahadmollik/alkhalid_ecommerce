from django.core.management.base import BaseCommand
from store.models import Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Assign placeholder images to products'

    def handle(self, *args, **options):
        # Define the mapping of product names to image files
        image_mapping = {
            'Wireless Bluetooth Headphones': 'wireless_bluetooth_headphones.jpg',
            'Smartphone Stand': 'smartphone_stand.jpg',
            'LED Desk Lamp': 'led_desk_lamp.jpg',
            'Electric Toothbrush': 'electric_toothbrush.jpg',
            '4K Webcam': '4k_webcam.jpg',
            'Wireless Charging Pad': 'wireless_charging_pad.jpg',
            'Classic Cotton T-Shirt': 'classic_cotton_t-shirt.jpg',
            'Denim Jacket': 'denim_jacket.jpg',
            'Running Shoes': 'running_shoes.jpg',
            'Winter Wool Scarf': 'winter_wool_scarf.jpg',
            'Python Programming Guide': 'python_programming_guide.jpg',
            'Web Development Handbook': 'web_development_handbook.jpg',
            'Digital Marketing Essentials': 'digital_marketing_essentials.jpg',
            'Yoga Mat': 'yoga_mat.jpg',
            'Water Bottle': 'water_bottle.jpg',
            'Camping Backpack': 'camping_backpack.jpg',
            'Vitamin C Serum': 'vitamin_c_serum.jpg',
            'Essential Oil Diffuser': 'essential_oil_diffuser.jpg',
            'Memory Foam Pillow': 'memory_foam_pillow.jpg',
            'Kitchen Knife Set': 'kitchen_knife_set.jpg',
            'Indoor Plant Pot Set': 'indoor_plant_pot_set.jpg'
        }

        updated_count = 0
        for product_name, image_filename in image_mapping.items():
            try:
                product = Product.objects.get(name=product_name)
                # Set the image field to the path relative to MEDIA_ROOT
                product.image = f'products/{image_filename}'
                product.save()
                self.stdout.write(f'Assigned {image_filename} to {product_name}')
                updated_count += 1
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Product "{product_name}" not found')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error assigning image to {product_name}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully assigned images to {updated_count} products!'
            )
        )
