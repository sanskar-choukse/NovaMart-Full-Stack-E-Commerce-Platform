from decimal import Decimal
from django.conf import settings
from apps.products.models import Product


class SessionCart:
    """Session-based cart for guest users"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, update_quantity=False):
        """Add product to cart or update quantity"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.get_price)
            }
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product):
        """Remove product from cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        """Save cart to session"""
        self.session.modified = True
    
    def clear(self):
        """Clear cart"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def __iter__(self):
        """Iterate over cart items"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        # Create a separate dict for iteration (don't modify self.cart)
        cart_items = []
        
        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                item = {
                    'product': product,
                    'quantity': self.cart[product_id]['quantity'],
                    'price': Decimal(self.cart[product_id]['price']),
                }
                item['total_price'] = item['price'] * item['quantity']
                cart_items.append(item)
        
        return iter(cart_items)
    
    def __len__(self):
        """Count all items in cart"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Calculate total price"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
