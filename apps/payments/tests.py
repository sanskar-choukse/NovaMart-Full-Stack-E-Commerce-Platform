from django.test import TestCase
from apps.users.models import User
from apps.orders.models import Order
from .models import Payment


class PaymentModelTest(TestCase):
    """Test Payment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone='1234567890',
            address='Test Address',
            city='Test City',
            state='Test State',
            pincode='123456',
            total_amount=1000.00
        )
    
    def test_payment_creation(self):
        """Test payment is created correctly"""
        payment = Payment.objects.create(
            order=self.order,
            payment_method='razorpay',
            payment_id='pay_test123',
            amount=1000.00,
            status='completed'
        )
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.status, 'completed')
