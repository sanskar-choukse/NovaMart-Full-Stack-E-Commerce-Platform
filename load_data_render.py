"""
Manual script to load data on Render
Use this if build.sh doesn't automatically load data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from django.core.management import call_command
from apps.products.models import Product

print("Checking product count...")
count = Product.objects.count()
print(f"Current products: {count}")

if count == 0:
    print("\nLoading products from DummyJSON API...")
    call_command('load_dummyjson_products')
    print(f"\n✓ Done! Total products: {Product.objects.count()}")
else:
    print("\n✓ Products already exist. No action needed.")
