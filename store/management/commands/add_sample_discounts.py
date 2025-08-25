from django.core.management.base import BaseCommand
from store.models import Product
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Add sample original prices to products to demonstrate discount functionality'

    def handle(self, *args, **options):
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            # Generate a random original price 10-50% higher than current price
            discount_percentage = random.randint(10, 50)
            original_price = product.price * Decimal(100 + discount_percentage) / Decimal(100)
            
            # Round to 2 decimal places
            product.original_price = original_price.quantize(Decimal('0.01'))
            product.save()
            updated_count += 1
            
            self.stdout.write(
                f'Updated {product.name}: Original ৳{product.original_price} → Current ৳{product.price} ({product.discount_percentage}% OFF)'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} products with original prices!')
        )
