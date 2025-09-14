from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Create sample hierarchical categories for testing'

    def handle(self, *args, **options):
        # Clear existing categories
        Category.objects.all().delete()
        
        # Create Electronics category with subcategories
        electronics = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
        
        # Mobile subcategory
        mobile = Category.objects.create(
            name='Mobile',
            description='Mobile phones and accessories',
            parent=electronics
        )
        
        # Mobile sub-subcategories
        Category.objects.create(
            name='Android',
            description='Android smartphones',
            parent=mobile
        )
        
        Category.objects.create(
            name='iPhone',
            description='Apple iPhones',
            parent=mobile
        )
        
        Category.objects.create(
            name='Accessories',
            description='Mobile accessories like cases, chargers',
            parent=mobile
        )
        
        # Computers subcategory
        computers = Category.objects.create(
            name='Computers',
            description='Desktop and laptop computers',
            parent=electronics
        )
        
        Category.objects.create(
            name='Laptops',
            description='Portable computers',
            parent=computers
        )
        
        Category.objects.create(
            name='Desktops',
            description='Desktop computers',
            parent=computers
        )
        
        # Create Clothing category with subcategories
        clothing = Category.objects.create(
            name='Clothing',
            description='Fashion and apparel'
        )
        
        # Men's clothing
        mens = Category.objects.create(
            name="Men's Clothing",
            description='Clothing for men',
            parent=clothing
        )
        
        Category.objects.create(
            name='Shirts',
            description='Men\'s shirts',
            parent=mens
        )
        
        Category.objects.create(
            name='Pants',
            description='Men\'s pants and trousers',
            parent=mens
        )
        
        # Women's clothing
        womens = Category.objects.create(
            name="Women's Clothing",
            description='Clothing for women',
            parent=clothing
        )
        
        Category.objects.create(
            name='Dresses',
            description='Women\'s dresses',
            parent=womens
        )
        
        Category.objects.create(
            name='Tops',
            description='Women\'s tops and blouses',
            parent=womens
        )
        
        # Create Books category with subcategories
        books = Category.objects.create(
            name='Books',
            description='Books and publications'
        )
        
        Category.objects.create(
            name='Fiction',
            description='Fiction books and novels',
            parent=books
        )
        
        Category.objects.create(
            name='Non-Fiction',
            description='Non-fiction books',
            parent=books
        )
        
        Category.objects.create(
            name='Technical',
            description='Technical and programming books',
            parent=books
        )
        
        # Create Sports category
        sports = Category.objects.create(
            name='Sports & Outdoors',
            description='Sports equipment and outdoor gear'
        )
        
        Category.objects.create(
            name='Fitness',
            description='Fitness equipment and gear',
            parent=sports
        )
        
        Category.objects.create(
            name='Outdoor',
            description='Outdoor activities equipment',
            parent=sports
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {Category.objects.count()} categories with hierarchical structure'
            )
        )
        
        # Print the hierarchy
        self.stdout.write('\nCategory Hierarchy:')
        for root_category in Category.get_root_categories():
            self._print_category_tree(root_category, 0)
    
    def _print_category_tree(self, category, level):
        indent = '  ' * level
        self.stdout.write(f'{indent}- {category.name}')
        for child in category.children.all():
            self._print_category_tree(child, level + 1)
