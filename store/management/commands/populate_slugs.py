from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populate slug fields for existing categories and products'

    def handle(self, *args, **options):
        # Populate category slugs
        categories_updated = 0
        for category in Category.objects.all():
            if not category.slug:
                category.slug = slugify(category.name)
                category.save()
                categories_updated += 1
                self.stdout.write(f'Updated category: {category.name} -> {category.slug}')

        # Populate product slugs
        products_updated = 0
        for product in Product.objects.all():
            if not product.slug:
                base_slug = slugify(product.name)
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                product.slug = slug
                product.save()
                products_updated += 1
                self.stdout.write(f'Updated product: {product.name} -> {product.slug}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {categories_updated} categories and {products_updated} products with slugs'
            )
        )
