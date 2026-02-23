"""
Clear all Django sessions to fix cart issues
Run: python clear_sessions.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.contrib.sessions.models import Session

# Delete all sessions
count = Session.objects.all().count()
Session.objects.all().delete()

print(f'✅ Cleared {count} sessions')
print('✅ Cart data reset')
print('✅ Please refresh your browser and try again')
print('\nNote: You may need to login again if you were logged in.')
