from django.test import TestCase
from apps.users.models import User
from apps.products.models import Category, Product
from .models import Cart, CartItem


class CartModelTest(TestCase):
    """Test Cart model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Laptop',
            price=1000.00,
            stock=10
        )
        self.cart = Cart.objects.create(user=self.user)
    
    def test_cart_creation(self):
        """Test cart is created correctly"""
        self.assertEqual(self.cart.user, self.user)
    
    def test_add_item_to_cart(self):
        """Test adding item to cart"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(self.cart.total_items, 2)
        self.assertEqual(cart_item.total_price, 2000.00)
