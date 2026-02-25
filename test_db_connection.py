"""
Test PostgreSQL database connection on Render
Run this to verify your database is properly connected
"""
import os
import sys
import django

# Set production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

try:
    django.setup()
    from django.db import connection
    from apps.products.models import Product, Category
    
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Test 1: Basic connection
    print("\n[1] Testing PostgreSQL connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✓ Connected to PostgreSQL")
            print(f"  Version: {version[:50]}...")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)
    
    # Test 2: Check migrations
    print("\n[2] Checking migrations...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations;")
            count = cursor.fetchone()[0]
            print(f"✓ Migrations table accessible: {count} migrations applied")
    except Exception as e:
        print(f"✗ Migrations check failed: {e}")
    
    # Test 3: Check tables
    print("\n[3] Checking application tables...")
    try:
        category_count = Category.objects.count()
        product_count = Product.objects.count()
        print(f"✓ Categories table: {category_count} records")
        print(f"✓ Products table: {product_count} records")
        
        if product_count == 0:
            print("\n⚠ WARNING: No products found!")
            print("  Run: python manage.py load_dummyjson_products")
    except Exception as e:
        print(f"✗ Table check failed: {e}")
    
    # Test 4: Check environment variables
    print("\n[4] Checking environment variables...")
    required_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DJANGO_SETTINGS_MODULE': os.getenv('DJANGO_SETTINGS_MODULE'),
        'CLOUDINARY_CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    }
    
    for var, value in required_vars.items():
        if value:
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET")
    
    print("\n" + "=" * 60)
    print("✓ DATABASE CONNECTION TEST COMPLETED")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
