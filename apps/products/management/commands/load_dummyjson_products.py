import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.products.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Load products from DummyJSON API (100+ products)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching products from DummyJSON API...')
        
        try:
            # Fetch all products from DummyJSON API
            response = requests.get('https://dummyjson.com/products?limit=100')
            response.raise_for_status()
            data = response.json()
            products_data = data['products']
            
            self.stdout.write(f'Found {len(products_data)} products')
            
            # Create categories and products
            created_products = 0
            updated_products = 0
            
            for item in products_data:
                # Get or create category
                category_name = item['category'].title()
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        'slug': slugify(category_name),
                        'description': f'{category_name} products',
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(f'Created category: {category_name}')
                
                # Create or update product
                product_slug = slugify(item['title']) + f"-{item['id']}"
                
                # Calculate discount price if discount exists
                discount_price = None
                if item.get('discountPercentage', 0) > 0:
                    discount = item['discountPercentage'] / 100
                    discount_price = round(item['price'] * (1 - discount), 2)
                
                # Check if product exists
                product, created = Product.objects.update_or_create(
                    slug=product_slug,
                    defaults={
                        'category': category,
                        'name': item['title'][:200],
                        'description': item['description'],
                        'price': item['price'],
                        'discount_price': discount_price,
                        'stock': item.get('stock', 50),
                        'is_active': True,
                        'is_featured': item.get('rating', 0) >= 4.5,
                    }
                )
                
                # Download and save thumbnail image
                if created or not product.image:
                    try:
                        # Use thumbnail image
                        img_url = item.get('thumbnail') or item.get('images', [None])[0]
                        if img_url:
                            img_response = requests.get(img_url, timeout=10)
                            if img_response.status_code == 200:
                                img_name = f"{product_slug}.jpg"
                                product.image.save(
                                    img_name,
                                    ContentFile(img_response.content),
                                    save=True
                                )
                                self.stdout.write(f'  ✓ Downloaded image for: {item["title"][:50]}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'  ✗ Failed to download image: {str(e)}')
                        )
                
                if created:
                    created_products += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Created: {item["title"][:60]}')
                    )
                else:
                    updated_products += 1
                    self.stdout.write(f'  → Updated: {item["title"][:60]}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Completed! Created: {created_products}, Updated: {updated_products}'
                )
            )
            self.stdout.write(f'Total products in database: {Product.objects.count()}')
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data from API: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
