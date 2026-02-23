from django.test import TestCase
from apps.users.models import User
from apps.products.models import Category, Product
from .models import Order, OrderItem


class OrderModelTest(TestCase):
    """Test Order model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Laptop',
            price=1000.00,
            stock=10
        )
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
    
    def test_order_creation(self):
        """Test order is created correctly"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_amount, 1000.00)
    
    def test_order_item_creation(self):
        """Test order item creation"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=1000.00,
            quantity=2
        )
        self.assertEqual(order_item.total_price, 2000.00)
