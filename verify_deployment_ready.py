"""
Pre-deployment verification script
Run this locally to ensure everything is configured correctly
"""
import os
from pathlib import Path

print("=" * 70)
print("DEPLOYMENT READINESS CHECK")
print("=" * 70)

issues = []
warnings = []
success = []

# Check 1: Requirements file
print("\n[1] Checking requirements.txt...")
req_file = Path("requirements.txt")
if req_file.exists():
    content = req_file.read_text()
    if "cloudinary" in content and "django-cloudinary-storage" in content:
        success.append("✓ Cloudinary packages in requirements.txt")
    else:
        issues.append("✗ Cloudinary packages missing from requirements.txt")
    
    if "psycopg2-binary" in content:
        success.append("✓ PostgreSQL driver (psycopg2-binary) present")
    else:
        issues.append("✗ PostgreSQL driver missing")
else:
    issues.append("✗ requirements.txt not found")

# Check 2: Build script
print("\n[2] Checking build.sh...")
build_file = Path("build.sh")
if build_file.exists():
    content = build_file.read_text()
    if "load_dummyjson_products" in content:
        success.append("✓ Data loading command in build.sh")
    else:
        warnings.append("⚠ Data loading not in build.sh (products won't auto-load)")
else:
    issues.append("✗ build.sh not found")

# Check 3: Settings files
print("\n[3] Checking Django settings...")
prod_settings = Path("config/settings/prod.py")
base_settings = Path("config/settings/base.py")

if prod_settings.exists():
    content = prod_settings.read_text()
    if "dj_database_url" in content:
        success.append("✓ Production settings configured for PostgreSQL")
    else:
        issues.append("✗ Production settings missing database configuration")
else:
    issues.append("✗ config/settings/prod.py not found")

if base_settings.exists():
    content = base_settings.read_text()
    if "cloudinary" in content.lower():
        success.append("✓ Cloudinary configured in base settings")
    else:
        warnings.append("⚠ Cloudinary not configured in settings")
else:
    issues.append("✗ config/settings/base.py not found")

# Check 4: Management commands
print("\n[4] Checking data loading commands...")
load_cmd = Path("apps/products/management/commands/load_dummyjson_products.py")
if load_cmd.exists():
    success.append("✓ load_dummyjson_products command exists")
else:
    issues.append("✗ Data loading command missing")

# Check 5: Test scripts
print("\n[5] Checking deployment scripts...")
if Path("test_db_connection.py").exists():
    success.append("✓ Database test script available")
else:
    warnings.append("⚠ test_db_connection.py not found")

if Path("load_data_render.py").exists():
    success.append("✓ Manual data loading script available")
else:
    warnings.append("⚠ load_data_render.py not found")

# Check 6: Render configuration
print("\n[6] Checking render.yaml...")
render_yaml = Path("render.yaml")
if render_yaml.exists():
    content = render_yaml.read_text()
    if "CLOUDINARY" in content:
        success.append("✓ Cloudinary variables in render.yaml")
    else:
        warnings.append("⚠ Cloudinary variables not in render.yaml")
    
    if "DATABASE_URL" in content:
        success.append("✓ Database configuration in render.yaml")
    else:
        issues.append("✗ DATABASE_URL not in render.yaml")
else:
    warnings.append("⚠ render.yaml not found")

# Print results
print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

if success:
    print("\n✅ SUCCESS:")
    for item in success:
        print(f"  {item}")

if warnings:
    print("\n⚠️  WARNINGS:")
    for item in warnings:
        print(f"  {item}")

if issues:
    print("\n❌ ISSUES (MUST FIX):")
    for item in issues:
        print(f"  {item}")

print("\n" + "=" * 70)

if issues:
    print("❌ NOT READY FOR DEPLOYMENT - Fix issues above")
    print("=" * 70)
    exit(1)
elif warnings:
    print("⚠️  READY WITH WARNINGS - Review warnings above")
    print("=" * 70)
    exit(0)
else:
    print("✅ READY FOR DEPLOYMENT!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Get Cloudinary credentials from https://cloudinary.com")
    print("2. Add to Render environment variables:")
    print("   - CLOUDINARY_CLOUD_NAME")
    print("   - CLOUDINARY_API_KEY")
    print("   - CLOUDINARY_API_SECRET")
    print("3. Push code to trigger deployment")
    print("4. Run test_db_connection.py on Render to verify")
    exit(0)
