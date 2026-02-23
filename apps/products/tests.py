from django.test import TestCase
from .models import Category, Product


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )
    
    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.slug, 'electronics')
    
    def test_category_str(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), 'Electronics')


class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Laptop',
            description='High-end laptop',
            price=1000.00,
            stock=10
        )
    
    def test_product_creation(self):
        """Test product is created correctly"""
        self.assertEqual(self.product.name, 'Laptop')
        self.assertEqual(self.product.price, 1000.00)
        self.assertEqual(self.product.slug, 'laptop')
    
    def test_product_in_stock(self):
        """Test product stock check"""
        self.assertTrue(self.product.is_in_stock)
    
    def test_discount_percentage(self):
        """Test discount calculation"""
        self.product.discount_price = 800.00
        self.product.save()
        self.assertEqual(self.product.discount_percentage, 20)
