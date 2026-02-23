"""
Reset all users - Delete all and create fresh admin
Run: python reset_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

print("=" * 60)
print("RESETTING ALL USERS")
print("=" * 60)

# Show current users
print("\nCurrent users:")
for user in User.objects.all():
    print(f"  - {user.username} ({user.email})")

# Delete all users
count = User.objects.count()
User.objects.all().delete()
print(f"\n✅ Deleted {count} users")

# Create new admin
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
print("\n✅ Created new admin user:")
print(f"   Username: admin")
print(f"   Password: admin123")
print(f"   Email: admin@example.com")

print("\n" + "=" * 60)
print("✅ USER RESET COMPLETE!")
print("=" * 60)
print("\nYou can now login with:")
print("  Username: admin")
print("  Password: admin123")
print("\nLogin at: http://localhost:8000/admin")
