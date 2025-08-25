from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from store.models import Order, OrderItem, Product, DeliveryOption
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate sample orders for analytics testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of sample orders to create'
        )

    def handle(self, *args, **options):
        order_count = options['count']
        
        # Get products and delivery options
        products = list(Product.objects.all())
        delivery_options = list(DeliveryOption.objects.filter(is_active=True))
        
        if not products:
            self.stdout.write(
                self.style.ERROR('No products found. Please create some products first.')
            )
            return
        
        if not delivery_options:
            # Create a default delivery option
            delivery_option = DeliveryOption.objects.create(
                name='Standard Delivery',
                description='Standard delivery within 3-5 business days',
                price=Decimal('5.00'),
                is_active=True,
                order=1
            )
            delivery_options = [delivery_option]
        
        # Sample customer data
        customers = [
            {'name': 'John Doe', 'email': 'john@example.com', 'phone': '123-456-7890'},
            {'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '123-456-7891'},
            {'name': 'Bob Johnson', 'email': 'bob@example.com', 'phone': '123-456-7892'},
            {'name': 'Alice Brown', 'email': 'alice@example.com', 'phone': '123-456-7893'},
            {'name': 'Charlie Wilson', 'email': 'charlie@example.com', 'phone': '123-456-7894'},
        ]
        
        addresses = [
            '123 Main St, Anytown, USA 12345',
            '456 Oak Ave, Somewhere, USA 67890',
            '789 Pine Rd, Elsewhere, USA 54321',
            '321 Elm St, Nowhere, USA 98765',
            '654 Maple Dr, Anywhere, USA 13579',
        ]
        
        statuses = ['pending', 'confirmed', 'shipped', 'delivered']
        payment_methods = ['cash_on_delivery', 'online_payment']
        
        orders_created = 0
        
        for i in range(order_count):
            # Random date within last 90 days
            days_ago = random.randint(0, 90)
            order_date = timezone.now() - timedelta(days=days_ago)
            
            # Random customer data
            customer = random.choice(customers)
            delivery_option = random.choice(delivery_options)
            
            # Calculate order items
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, min(num_items, len(products)))
            
            subtotal = Decimal('0.00')
            order_items_data = []
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price
                total = price * quantity
                subtotal += total
                
                order_items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price
                })
            
            delivery_fee = delivery_option.price
            total_amount = subtotal + delivery_fee
            
            # Create order
            order = Order.objects.create(
                customer_name=customer['name'],
                customer_email=customer['email'],
                customer_phone=customer['phone'],
                shipping_address=random.choice(addresses),
                delivery_option=delivery_option,
                delivery_fee=delivery_fee,
                subtotal=subtotal,
                total_amount=total_amount,
                status=random.choice(statuses),
                payment_method=random.choice(payment_methods),
                notes=f'Sample order #{i+1}',
                created_at=order_date
            )
            
            # Create order items
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
            
            orders_created += 1
            
            if orders_created % 10 == 0:
                self.stdout.write(f'Created {orders_created} orders...')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {orders_created} sample orders for analytics!'
            )
        )
        
        # Display some stats
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(
            total=sum(order.total_amount for order in Order.objects.all())
        )
        
        self.stdout.write(f'Total orders in database: {total_orders}')
        self.stdout.write(f'Total revenue: ${total_revenue["total"] or 0:.2f}')
        self.stdout.write(
            self.style.WARNING(
                '\nAccess analytics at: /analytics/\n'
                '(Login as admin user required)'
            )
        )
