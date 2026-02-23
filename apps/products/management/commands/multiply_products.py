import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Multiply existing products to create more variety in each category'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of products to create per category (default: 10)'
        )

    def handle(self, *args, **kwargs):
        count_per_category = kwargs['count']
        
        self.stdout.write(f'Creating {count_per_category} products per category...')
        
        categories = Category.objects.all()
        
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found! Run load_fake_products first.'))
            return
        
        total_created = 0
        
        for category in categories:
            # Get existing products in this category
            existing_products = list(Product.objects.filter(category=category))
            
            if not existing_products:
                self.stdout.write(self.style.WARNING(f'No products in {category.name}, skipping...'))
                continue
            
            self.stdout.write(f'\nProcessing category: {category.name}')
            
            # Create variations
            for i in range(count_per_category):
                # Pick a random existing product as template
                template = random.choice(existing_products)
                
                # Create variations
                variations = [
                    'Premium', 'Deluxe', 'Classic', 'Modern', 'Vintage',
                    'Pro', 'Elite', 'Standard', 'Advanced', 'Basic',
                    'Plus', 'Ultra', 'Super', 'Mega', 'Special Edition'
                ]
                
                colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Gray', 'Navy', 'Brown']
                sizes = ['Small', 'Medium', 'Large', 'XL', 'XXL']
                
                # Generate unique name
                variation = random.choice(variations)
                color = random.choice(colors)
                
                new_name = f"{variation} {template.name[:100]} - {color}"
                new_slug = slugify(new_name) + f"-{random.randint(1000, 9999)}"
                
                # Check if slug exists
                if Product.objects.filter(slug=new_slug).exists():
                    continue
                
                # Create new product
                new_product = Product.objects.create(
                    category=category,
                    name=new_name[:200],
                    slug=new_slug,
                    description=template.description,
                    price=round(float(template.price) * random.uniform(0.8, 1.5), 2),
                    discount_price=round(float(template.price) * random.uniform(0.6, 0.9), 2) if random.choice([True, False]) else None,
                    stock=random.randint(10, 100),
                    is_active=True,
                    is_featured=random.choice([True, False, False, False]),  # 25% chance
                    image=template.image  # Reuse same image
                )
                
                total_created += 1
                self.stdout.write(f'  Created: {new_name[:60]}...')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {total_created} new products!')
        )
        self.stdout.write(f'Total products now: {Product.objects.count()}')
