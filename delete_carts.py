"""
Delete all carts from database
Run: python delete_carts.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.cart.models import Cart, CartItem

print("=" * 60)
print("DELETING ALL CARTS")
print("=" * 60)

# Count carts
cart_count = Cart.objects.count()
item_count = CartItem.objects.count()

print(f"\nCurrent data:")
print(f"  - Carts: {cart_count}")
print(f"  - Cart Items: {item_count}")

# Delete all
Cart.objects.all().delete()

print(f"\n✅ Deleted {cart_count} carts")
print(f"✅ Deleted {item_count} cart items")

print("\n" + "=" * 60)
print("✅ ALL CARTS DELETED!")
print("=" * 60)
