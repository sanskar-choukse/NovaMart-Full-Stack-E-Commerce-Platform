from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.cart.models import Cart, CartItem
from apps.cart.cart import SessionCart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    """Checkout view"""
    # Get cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product')
        total = cart.total
        
        if not cart_items.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart:cart_detail')
    else:
        return redirect('users:login')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = total
                order.save()
                
                # Create order items
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.get_price,
                        quantity=item.quantity
                    )
                    # Update product stock
                    item.product.stock -= item.quantity
                    item.product.save()
                
                # Clear cart
                cart_items.delete()
                
                # Redirect to payment
                return redirect('payments:payment', order_id=order.order_id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
            'phone': request.user.phone,
            'address': request.user.address,
            'city': request.user.city,
            'state': request.user.state,
            'pincode': request.user.pincode,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    """List user orders"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        order_id=order_id,
        user=request.user
    )
    return render(request, 'orders/order_detail.html', {'order': order})
