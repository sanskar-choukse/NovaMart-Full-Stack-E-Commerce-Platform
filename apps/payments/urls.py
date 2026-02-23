from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'payments'

urlpatterns = [
    path('payment/<uuid:order_id>/', views.payment_view, name='payment'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
    path('stripe/<uuid:order_id>/', views.stripe_payment, name='stripe_payment'),
    path('success/<uuid:order_id>/', views.payment_success, name='payment_success'),
    path('failed/<uuid:order_id>/', views.payment_failed, name='payment_failed'),
    path('test/', TemplateView.as_view(template_name='payments/payment_test.html'), name='test'),
]
