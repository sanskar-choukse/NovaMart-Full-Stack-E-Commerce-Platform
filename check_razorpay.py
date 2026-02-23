"""
Check Razorpay configuration
Run: python check_razorpay.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.conf import settings

print("=" * 70)
print("RAZORPAY CONFIGURATION CHECK")
print("=" * 70)

# Check if keys are configured
key_id = settings.RAZORPAY_KEY_ID
key_secret = settings.RAZORPAY_KEY_SECRET

print("\n1. Checking Environment Variables:")
print("-" * 70)

if key_id:
    print(f"✅ RAZORPAY_KEY_ID: {key_id[:15]}..." if len(key_id) > 15 else f"✅ RAZORPAY_KEY_ID: {key_id}")
    
    # Check if it's test or live key
    if key_id.startswith('rzp_test_'):
        print("   ℹ️  Mode: TEST MODE (Good for development)")
    elif key_id.startswith('rzp_live_'):
        print("   ⚠️  Mode: LIVE MODE (Use with caution!)")
    else:
        print("   ❌ Invalid Key ID format")
else:
    print("❌ RAZORPAY_KEY_ID: Not configured")

if key_secret:
    print(f"✅ RAZORPAY_KEY_SECRET: {'*' * 20} (Hidden)")
else:
    print("❌ RAZORPAY_KEY_SECRET: Not configured")

# Test Razorpay connection
print("\n2. Testing Razorpay Connection:")
print("-" * 70)

if key_id and key_secret:
    try:
        import razorpay
        client = razorpay.Client(auth=(key_id, key_secret))
        
        # Try to create a test order
        test_order = client.order.create({
            'amount': 100,  # ₹1.00
            'currency': 'INR',
            'payment_capture': 1
        })
        
        print("✅ Connection successful!")
        print(f"✅ Test order created: {test_order['id']}")
        print("✅ Razorpay API is working correctly")
        
    except razorpay.errors.BadRequestError as e:
        print(f"❌ Bad Request Error: {str(e)}")
        print("   Check if your API keys are correct")
    except razorpay.errors.SignatureVerificationError as e:
        print(f"❌ Signature Error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Make sure razorpay package is installed: pip install razorpay")
else:
    print("⚠️  Cannot test - Keys not configured")

# Check payment URLs
print("\n3. Payment URLs:")
print("-" * 70)
print("✅ Payment page: http://localhost:8000/payments/payment/<order_id>/")
print("✅ Callback URL: http://localhost:8000/payments/razorpay/callback/")
print("✅ Success page: http://localhost:8000/payments/success/<order_id>/")
print("✅ Failed page: http://localhost:8000/payments/failed/<order_id>/")

# Configuration summary
print("\n4. Configuration Summary:")
print("-" * 70)

if key_id and key_secret:
    if key_id.startswith('rzp_test_'):
        print("✅ Status: READY FOR TESTING")
        print("\nNext steps:")
        print("1. Go to: http://localhost:8000/shop/")
        print("2. Add a product to cart")
        print("3. Proceed to checkout")
        print("4. Use test card: 4111 1111 1111 1111")
        print("5. CVV: 123, Expiry: 12/25")
    else:
        print("⚠️  Status: CONFIGURED (Check mode)")
else:
    print("❌ Status: NOT CONFIGURED")
    print("\nTo configure:")
    print("1. Get API keys from: https://dashboard.razorpay.com/app/keys")
    print("2. Add to .env file:")
    print("   RAZORPAY_KEY_ID=rzp_test_your_key_id")
    print("   RAZORPAY_KEY_SECRET=your_key_secret")
    print("3. Restart server: python manage.py runserver")

print("\n" + "=" * 70)
print("For detailed setup guide, read: RAZORPAY_SETUP_GUIDE.md")
print("=" * 70)
