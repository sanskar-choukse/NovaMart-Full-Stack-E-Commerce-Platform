from django.db import models
from django.conf import settings
from apps.products.models import Product


class Cart(models.Model):
    """Cart model for logged-in users"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_items(self):
        """Get total number of items in cart"""
        items = self.items.all()
        if not items:
            return 0
        return sum(item.quantity for item in items)

    @property
    def subtotal(self):
        """Calculate cart subtotal"""
        items = self.items.all()
        if not items:
            return 0
        return sum(item.total_price for item in items)

    @property
    def total(self):
        """Calculate cart total (can add shipping, tax here)"""
        return self.subtotal


class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        """Calculate total price for this item"""
        return self.product.get_price * self.quantity
