# E-Commerce Platform - Django

A production-ready e-commerce web application built with Django, MySQL, and modern web technologies.

## Features

- User authentication & profiles
- Product catalog with categories
- Shopping cart (session & persistent)
- Order management
- Payment integration (Razorpay/Stripe test mode)
- Admin dashboard
- Responsive design
- Docker support

## Tech Stack

- Backend: Django 5.0+
- Database: MySQL 8.0+
- Frontend: HTML5, CSS3
- Payment: Razorpay/Stripe (Test Mode)
- Containerization: Docker

## Project Structure

```
ecommerce/
├── apps/
│   ├── users/          # Authentication & user profiles
│   ├── products/       # Product management
│   ├── cart/           # Shopping cart
│   ├── orders/         # Order processing
│   └── payments/       # Payment integration
├── config/             # Project settings
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
├── templates/          # HTML templates
├── docker/             # Docker configuration
└── requirements/       # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- pip
- virtualenv (recommended)

### Local Development Setup

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```

4. Create `.env` file in project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_NAME=ecommerce_db
   DATABASE_USER=root
   DATABASE_PASSWORD=your-password
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   
   # Razorpay (Test Mode)
   RAZORPAY_KEY_ID=your-test-key
   RAZORPAY_KEY_SECRET=your-test-secret
   
   # OR Stripe (Test Mode)
   STRIPE_PUBLIC_KEY=your-test-public-key
   STRIPE_SECRET_KEY=your-test-secret-key
   ```

5. Create MySQL database:
   ```sql
   CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Load sample data (optional):
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```

9. Run development server:
   ```bash
   python manage.py runserver
   ```

Visit: http://localhost:8000

### Docker Setup

1. Ensure Docker and Docker Compose are installed

2. Create `.env` file (same as above)

3. Build and run:
   ```bash
   docker-compose up --build
   ```

4. Run migrations in container:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

Visit: http://localhost:8000

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Django secret key | Yes |
| DEBUG | Debug mode (True/False) | Yes |
| DATABASE_NAME | MySQL database name | Yes |
| DATABASE_USER | MySQL username | Yes |
| DATABASE_PASSWORD | MySQL password | Yes |
| DATABASE_HOST | MySQL host | Yes |
| DATABASE_PORT | MySQL port | Yes |
| RAZORPAY_KEY_ID | Razorpay test key | Optional |
| RAZORPAY_KEY_SECRET | Razorpay test secret | Optional |
| STRIPE_PUBLIC_KEY | Stripe test public key | Optional |
| STRIPE_SECRET_KEY | Stripe test secret key | Optional |

## Payment Gateway Setup

### Razorpay (Test Mode)

1. Sign up at https://razorpay.com
2. Get test API keys from Dashboard
3. Add keys to `.env` file
4. Test cards: https://razorpay.com/docs/payments/payments/test-card-details/

### Stripe (Test Mode)

1. Sign up at https://stripe.com
2. Get test API keys from Dashboard
3. Add keys to `.env` file
4. Test card: 4242 4242 4242 4242

## Running Tests

```bash
python manage.py test
```

With coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## Admin Access

Access admin panel at: http://localhost:8000/admin

## API Endpoints (Optional)

- `/api/products/` - Product list
- `/api/cart/` - Cart operations
- `/api/orders/` - Order management

## Deployment

### Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong SECRET_KEY
- [ ] Configure static files serving
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Database backups
- [ ] Monitor error tracking

### Deployment Options

- AWS EC2 + RDS
- DigitalOcean Droplet
- Heroku
- Google Cloud Platform
- Azure

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
