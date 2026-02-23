from .cart import SessionCart


def cart_context(request):
    """Add cart to template context"""
    if request.user.is_authenticated:
        # For logged-in users, use database cart
        from .models import Cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {
            'cart': cart,
            'cart_total_items': cart.total_items,
            'cart_total': float(cart.total) if cart.total else 0
        }
    else:
        # For guest users, use session cart
        cart = SessionCart(request)
        total = cart.get_total_price()
        return {
            'cart': cart,
            'cart_total_items': len(cart),
            'cart_total': float(total) if total else 0
        }
