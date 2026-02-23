"""
Complete database reset - Delete everything and reload
Run: python reset_database.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User
from apps.products.models import Product, Category
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment

print("=" * 70)
print("COMPLETE DATABASE RESET")
print("=" * 70)

print("\nCurrent database contents:")
print(f"  - Users: {User.objects.count()}")
print(f"  - Products: {Product.objects.count()}")
print(f"  - Categories: {Category.objects.count()}")
print(f"  - Carts: {Cart.objects.count()}")
print(f"  - Orders: {Order.objects.count()}")
print(f"  - Payments: {Payment.objects.count()}")

print("\n" + "-" * 70)
print("DELETING ALL DATA...")
print("-" * 70)

# Delete in correct order (to avoid foreign key issues)
Payment.objects.all().delete()
print("✅ Deleted all payments")

Order.objects.all().delete()
print("✅ Deleted all orders")

Cart.objects.all().delete()
print("✅ Deleted all carts")

Product.objects.all().delete()
print("✅ Deleted all products")

Category.objects.all().delete()
print("✅ Deleted all categories")

User.objects.all().delete()
print("✅ Deleted all users")

print("\n" + "-" * 70)
print("CREATING FRESH DATA...")
print("-" * 70)

# Create admin user
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
print("✅ Created admin user (admin/admin123)")

print("\n" + "=" * 70)
print("✅ DATABASE RESET COMPLETE!")
print("=" * 70)

print("\nNext steps:")
print("1. Load products: python manage.py load_fake_products")
print("2. Login at: http://localhost:8000/admin")
print("   Username: admin")
print("   Password: admin123")
