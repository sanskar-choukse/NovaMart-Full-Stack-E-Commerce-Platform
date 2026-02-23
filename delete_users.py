"""
Delete all users from database (except superusers)
Run: python delete_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

print("Current users in database:")
print("-" * 50)
for user in User.objects.all():
    status = "SUPERUSER" if user.is_superuser else "Regular User"
    print(f"- {user.username} ({user.email}) - {status}")

print("\n" + "=" * 50)
choice = input("\nWhat do you want to delete?\n1. All regular users (keep admin)\n2. All users (including admin)\n3. Cancel\n\nEnter choice (1/2/3): ")

if choice == "1":
    # Delete only regular users
    regular_users = User.objects.filter(is_superuser=False)
    count = regular_users.count()
    regular_users.delete()
    print(f"\n✅ Deleted {count} regular users")
    print("✅ Admin users preserved")
    
elif choice == "2":
    # Delete all users
    count = User.objects.count()
    User.objects.all().delete()
    print(f"\n✅ Deleted all {count} users")
    print("⚠️  You'll need to create a new admin user")
    print("   Run: python create_admin.py")
    
else:
    print("\n❌ Cancelled - No users deleted")

print("\nRemaining users:")
print("-" * 50)
remaining = User.objects.all()
if remaining.exists():
    for user in remaining:
        status = "SUPERUSER" if user.is_superuser else "Regular User"
        print(f"- {user.username} ({user.email}) - {status}")
else:
    print("No users in database")
