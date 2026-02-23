"""
Check if product images are configured correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.products.models import Product

print("Checking product images...\n")

products = Product.objects.all()[:5]

for product in products:
    print(f"Product: {product.name[:50]}")
    print(f"Image field: {product.image}")
    print(f"Image URL: {product.image.url if product.image else 'No image'}")
    print(f"Image path: {product.image.path if product.image else 'No image'}")
    print(f"File exists: {os.path.exists(product.image.path) if product.image else False}")
    print("-" * 80)
