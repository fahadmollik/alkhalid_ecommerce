## Updates (2025)

- Added custom admin panel (`custom_admin` app) for advanced management
- DeliveryOption CRUD management for admin (settings section)
- Dynamic site branding and contact info (editable from admin)
- PostgreSQL support and .env configuration for secrets and database
- Improved UI alignment for admin buttons (DeliveryOption, etc.)
- Enhanced security and production readiness instructions
- Updated .gitignore for Django, media/static, venv, and secrets

---

# Django E-Commerce Application

A comprehensive e-commerce web application built with Django, featuring a responsive design using Bootstrap, product catalog management, shopping cart functionality, and a custom admin interface.

## Features

### Frontend Features
- Responsive design (Bootstrap 5)
- Dynamic hero carousel banners
- Product catalog with categories, best sellers, and featured products
- Shopping cart (no authentication required)
- Cash-on-delivery checkout
- Product details with image galleries
- Dynamic branding and contact info (admin configurable)

### Admin Features
- Custom admin panel (`custom_admin` app)
- DeliveryOption management (CRUD)
- Product/category/order/banner management
- Inventory tracking and low stock alerts
- Analytics dashboard
- Site branding and settings management

### Technical Features
- SQLite for development, PostgreSQL ready for production
- .env support for secrets and config
- Image optimization (Pillow)
- Security: CSRF, admin-only access, session security
- Performance: caching, optimized queries, pagination
- SEO-friendly URLs

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Instructions
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` for secrets and database
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the development server: `python manage.py runserver`

## Usage

- Visit `/` for the storefront
- Visit `/custom_admin/` for the custom admin panel
- Manage products, categories, orders, banners, and delivery options
- Configure site branding and contact info from admin settings

## Project Structure

- `ecommerce_project/` - Django project settings
- `store/` - Main e-commerce app
- `custom_admin/` - Custom admin app (DeliveryOption, branding, analytics, etc.)
- `templates/` - HTML templates
- `static/` - CSS, JS, images
- `media/` - Uploaded images
- `requirements.txt` - Python dependencies
- `.env` - Environment variables

## Environment Variables Example
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

## Key Models
- Product, Category, Order, DeliveryOption, HeroBanner, SiteSettings

## Security & Production
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` for production
- Use PostgreSQL and proper `.env` secrets
- Collect static files: `python manage.py collectstatic`
- Configure media/static serving for production

## License
MIT or custom license

---

For support, contact the admin via the site settings email/phone.

This project is ready for customization and deployment. For advanced features (payments, reviews, user accounts), see the customization section in the codebase.
