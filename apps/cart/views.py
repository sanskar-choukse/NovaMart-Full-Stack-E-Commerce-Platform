from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.products.models import Product
from .models import Cart, CartItem
from .cart import SessionCart


def cart_detail(request):
    """Display cart contents"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product')
        total = cart.total
    else:
        cart = SessionCart(request)
        cart_items = list(cart)
        total = cart.get_total_price()
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def cart_add(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, 'Not enough stock available.')
        return redirect('products:detail', slug=product.slug)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        cart = SessionCart(request)
        cart.add(product=product, quantity=quantity)
    
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """Update cart item quantity"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, 'Not enough stock available.')
        return redirect('cart:cart_detail')
    
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    else:
        cart = SessionCart(request)
        if quantity > 0:
            cart.add(product=product, quantity=quantity, update_quantity=True)
        else:
            cart.remove(product)
    
    messages.success(request, 'Cart updated.')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove product from cart"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, product=product).delete()
    else:
        cart = SessionCart(request)
        cart.remove(product)
    
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('cart:cart_detail')
