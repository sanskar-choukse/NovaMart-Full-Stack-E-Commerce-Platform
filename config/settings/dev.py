"""
Development settings
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.ngrok.io']

# Use SQLite for development (no MySQL needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug Toolbar (optional - comment out if not installed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Development email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security settings for development (allow Razorpay)
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'

# Disable some security features for development
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Allow iframes from Razorpay
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Disable password validators for easier development
AUTH_PASSWORD_VALIDATORS = []
