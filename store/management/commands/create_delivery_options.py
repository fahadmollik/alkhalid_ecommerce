from django.core.management.base import BaseCommand
from store.models import DeliveryOption

class Command(BaseCommand):
    help = 'Create sample delivery options'

    def handle(self, *args, **options):
        # Clear existing delivery options
        DeliveryOption.objects.all().delete()
        
        # Create delivery options
        delivery_options = [
            {
                'name': 'In City Delivery',
                'description': 'Delivery within city limits (3-5 business days)',
                'price': 20.00,
                'order': 1
            },
            {
                'name': 'Outside City Delivery', 
                'description': 'Delivery outside city limits (5-7 business days)',
                'price': 10.00,
                'order': 2
            },
            {
                'name': 'Express Delivery',
                'description': 'Fast delivery within city (1-2 business days)',
                'price': 35.00,
                'order': 3
            }
        ]
        
        for option_data in delivery_options:
            delivery_option = DeliveryOption.objects.create(**option_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created delivery option: {delivery_option.name} - ${delivery_option.price}')
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample delivery options!'))
