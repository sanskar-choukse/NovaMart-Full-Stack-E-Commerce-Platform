"""
Delete all orders from database
Run: python delete_orders.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.orders.models import Order, OrderItem

print("=" * 60)
print("DELETING ALL ORDERS")
print("=" * 60)

# Count orders
order_count = Order.objects.count()
item_count = OrderItem.objects.count()

print(f"\nCurrent data:")
print(f"  - Orders: {order_count}")
print(f"  - Order Items: {item_count}")

# Delete all
Order.objects.all().delete()

print(f"\n✅ Deleted {order_count} orders")
print(f"✅ Deleted {item_count} order items")

print("\n" + "=" * 60)
print("✅ ALL ORDERS DELETED!")
print("=" * 60)
