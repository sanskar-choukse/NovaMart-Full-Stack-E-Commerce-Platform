import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.products.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Load products from Fake Store API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching products from Fake Store API...')
        
        try:
            # Fetch products from API
            response = requests.get('https://fakestoreapi.com/products')
            response.raise_for_status()
            products_data = response.json()
            
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
                product_slug = slugify(item['title'])
                
                # Check if product exists
                product, created = Product.objects.update_or_create(
                    slug=product_slug,
                    defaults={
                        'category': category,
                        'name': item['title'][:200],  # Limit to 200 chars
                        'description': item['description'],
                        'price': item['price'],
                        'stock': 50,  # Default stock
                        'is_active': True,
                        'is_featured': item['rating']['rate'] >= 4.0,  # Featured if rating >= 4
                    }
                )
                
                # Download and save image
                if created or not product.image:
                    try:
                        img_response = requests.get(item['image'], timeout=10)
                        if img_response.status_code == 200:
                            img_name = f"{product_slug}.jpg"
                            product.image.save(
                                img_name,
                                ContentFile(img_response.content),
                                save=True
                            )
                            self.stdout.write(f'Downloaded image for: {item["title"][:50]}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to download image: {str(e)}')
                        )
                
                if created:
                    created_products += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created product: {item["title"][:50]}')
                    )
                else:
                    updated_products += 1
                    self.stdout.write(f'Updated product: {item["title"][:50]}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nCompleted! Created: {created_products}, Updated: {updated_products}'
                )
            )
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data from API: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
