"""
Delete ALL users from database
Run: python delete_all_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

print("Users before deletion:")
print("-" * 50)
for user in User.objects.all():
    status = "SUPERUSER" if user.is_superuser else "Regular User"
    print(f"- {user.username} ({user.email}) - {status}")

# Delete all users
count = User.objects.count()
User.objects.all().delete()

print("\n" + "=" * 50)
print(f"✅ Deleted all {count} users from database")
print("=" * 50)

print("\nUsers after deletion:")
print("-" * 50)
remaining = User.objects.all()
if remaining.exists():
    for user in remaining:
        print(f"- {user.username}")
else:
    print("✅ No users in database - All deleted successfully!")

print("\n" + "=" * 50)
print("To create a new admin user, run:")
print("python create_admin.py")
print("=" * 50)
