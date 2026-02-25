#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Load initial data if database is empty
echo "Checking if products exist..."
PRODUCT_COUNT=$(python manage.py shell -c "from apps.products.models import Product; print(Product.objects.count())")
if [ "$PRODUCT_COUNT" -eq "0" ]; then
    echo "No products found. Loading initial data..."
    python manage.py load_dummyjson_products
    echo "✓ Products loaded successfully!"
else
    echo "✓ Products already exist ($PRODUCT_COUNT products). Skipping data load."
fi
