#  NovaMart- E-Commerce Platform

A full-stack online shopping application with user authentication, product management, cart, checkout, and payment integration.


---

## 🚀 Live Demo
🔗https://novamart-k3ka.onrender.com
---

## Core Features

- User registration, login, and profile management
- Product catalog with categories, search, and filtering
- Shopping cart (session-based and persistent)
- Order processing and tracking
- Payment integration (Razorpay & Stripe test mode)
- Admin dashboard for management
- Cloudinary media storage
- RESTful API endpoints

## Tech Stack

**Backend:** Django 5.0, Python 3.11+

**Database:** MySQL 8.0 (dev), PostgreSQL (production)

**Frontend:** HTML5, CSS3, Bootstrap 4

**Payment:** Razorpay, Stripe

**Storage:** Cloudinary (media), WhiteNoise (static)

**Server:** Gunicorn, Docker support

## Project Structure
```
ecommerce/
├── apps/                      # Django applications
│   ├── users/                # User authentication & profiles
│   ├── products/             # Product catalog & categories
│   ├── cart/                 # Shopping cart functionality
│   ├── orders/               # Order processing
│   └── payments/             # Payment gateway integration
├── config/                    # Project configuration
│   ├── settings/             # Split settings (base, dev, prod)
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── templates/                 # HTML templates
├── static/                    # Static files (CSS, JS)
├── media/                     # User uploads (local dev)
├── requirements/              # Dependencies (base, dev, prod)
└── manage.py                  # Django management script
```

## Key Models

- User (custom with address fields)
- Category & Product (with images, pricing, stock)
- Cart & CartItem
- Order & OrderItem
- Payment (transaction tracking)

## Deployment

- Docker & docker-compose ready
- Render.com compatible
- Environment-based configuration
- Automatic data loading scripts

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## License

MIT License
