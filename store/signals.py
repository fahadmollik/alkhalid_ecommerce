import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Product, Category, HeroBanner, SiteSettings


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    """Delete product image file when product is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Product)
def delete_old_product_image(sender, instance, **kwargs):
    """Delete old product image when a new one is uploaded."""
    if not instance.pk:
        return False

    try:
        old_image = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    if old_image and old_image != instance.image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=Category)
def delete_category_image(sender, instance, **kwargs):
    """Delete category image file when category is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Category)
def delete_old_category_image(sender, instance, **kwargs):
    """Delete old category image when a new one is uploaded."""
    if not instance.pk:
        return False

    try:
        old_image = Category.objects.get(pk=instance.pk).image
    except Category.DoesNotExist:
        return False

    if old_image and old_image != instance.image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=HeroBanner)
def delete_banner_image(sender, instance, **kwargs):
    """Delete banner image file when banner is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=HeroBanner)
def delete_old_banner_image(sender, instance, **kwargs):
    """Delete old banner image when a new one is uploaded."""
    if not instance.pk:
        return False

    try:
        old_image = HeroBanner.objects.get(pk=instance.pk).image
    except HeroBanner.DoesNotExist:
        return False

    if old_image and old_image != instance.image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=SiteSettings)
def delete_site_settings_images(sender, instance, **kwargs):
    """Delete logo and favicon files when site settings are deleted."""
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)
    
    if instance.favicon:
        if os.path.isfile(instance.favicon.path):
            os.remove(instance.favicon.path)


@receiver(pre_save, sender=SiteSettings)
def delete_old_site_settings_images(sender, instance, **kwargs):
    """Delete old logo and favicon when new ones are uploaded."""
    if not instance.pk:
        return False

    try:
        old_settings = SiteSettings.objects.get(pk=instance.pk)
    except SiteSettings.DoesNotExist:
        return False

    # Delete old logo if it's being replaced
    if old_settings.logo and old_settings.logo != instance.logo:
        if os.path.isfile(old_settings.logo.path):
            os.remove(old_settings.logo.path)
    
    # Delete old favicon if it's being replaced
    if old_settings.favicon and old_settings.favicon != instance.favicon:
        if os.path.isfile(old_settings.favicon.path):
            os.remove(old_settings.favicon.path)
