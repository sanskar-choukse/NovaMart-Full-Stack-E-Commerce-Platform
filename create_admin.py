"""
Quick script to create admin user
Run: python create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

# Create admin user
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Admin user created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Login at: http://localhost:8000/admin')
else:
    print(f'⚠️  Admin user already exists')
    print(f'Username: {username}')
    print(f'Password: {password}')
