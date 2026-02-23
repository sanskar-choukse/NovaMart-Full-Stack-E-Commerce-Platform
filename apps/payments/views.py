from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import razorpay
import stripe
import hmac
import hashlib
from apps.orders.models import Order
from .models import Payment


@login_required
def payment_view(request, order_id):
    """Payment page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.is_paid:
        messages.info(request, 'This order is already paid.')
        return redirect('orders:order_detail', order_id=order.order_id)
    
    # Choose payment gateway (Razorpay by default)
    payment_method = request.GET.get('method', 'razorpay')
    
    context = {
        'order': order,
        'payment_method': payment_method,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    
    if payment_method == 'razorpay':
        # Create Razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            'amount': int(order.total_amount * 100),  # Amount in paise
            'currency': 'INR',
            'payment_capture': 1
        })
        context['razorpay_order_id'] = razorpay_order['id']
    
    return render(request, 'payments/payment.html', context)


@csrf_exempt
@login_required
def razorpay_callback(request):
    """Razorpay payment callback"""
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        order_uuid = request.POST.get('order_uuid')
        
        # Verify signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)
            
            # Update order
            order = Order.objects.get(order_id=order_uuid)
            order.is_paid = True
            order.paid_at = timezone.now()
            order.status = 'processing'
            order.save()
            
            # Create payment record
            Payment.objects.create(
                order=order,
                payment_method='razorpay',
                payment_id=payment_id,
                amount=order.total_amount,
                status='completed',
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id,
                razorpay_signature=signature
            )
            
            messages.success(request, 'Payment successful!')
            return redirect('payments:payment_success', order_id=order.order_id)
        
        except Exception as e:
            messages.error(request, f'Payment verification failed: {str(e)}')
            return redirect('payments:payment_failed', order_id=order_uuid)
    
    return redirect('products:home')


@login_required
def stripe_payment(request, order_id):
    """Stripe payment processing"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),  # Amount in cents
                currency='usd',
                metadata={'order_id': str(order.order_id)}
            )
            
            # Update order
            order.is_paid = True
            order.paid_at = timezone.now()
            order.status = 'processing'
            order.save()
            
            # Create payment record
            Payment.objects.create(
                order=order,
                payment_method='stripe',
                payment_id=intent.id,
                amount=order.total_amount,
                status='completed',
                stripe_payment_intent_id=intent.id
            )
            
            messages.success(request, 'Payment successful!')
            return redirect('payments:payment_success', order_id=order.order_id)
        
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')
            return redirect('payments:payment_failed', order_id=order.order_id)
    
    return redirect('payments:payment', order_id=order.order_id)


@login_required
def payment_success(request, order_id):
    """Payment success page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'payments/payment_success.html', {'order': order})


@login_required
def payment_failed(request, order_id):
    """Payment failed page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'payments/payment_failed.html', {'order': order})
