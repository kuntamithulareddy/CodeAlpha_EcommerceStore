# CodeAlpha E-commerce Store

A beginner-friendly full-stack shopping website built with:
- Frontend: HTML, CSS, JavaScript
- Backend: Python + Django
- Database: SQLite (Django default)

## Features
- Product listing and product details
- Shopping cart (session-based)
- Checkout/order processing
- User registration, login, logout
- Order records saved in the database
- Django admin for managing products and orders

## 1. Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection only for installing Django

## 2. Setup (Windows)
Open this project folder in VS Code.

Open Terminal in VS Code and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

If PowerShell blocks activation, use Command Prompt terminal and run:
```bat
.venv\Scripts\activate.bat
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/
Sign in with the superuser you created.

## 3. Important
- This is a learning/demo project. Checkout records an order; it does not charge a real payment.
- Change `SECRET_KEY` and set `DEBUG = False` before any real public production deployment.
- SQLite database file `db.sqlite3` is created after migrations. It is not included in this ZIP.
- Never upload passwords, `.venv`, or real secret keys to GitHub.

## 4. GitHub
Create a repository named `CodeAlpha_EcommerceStore`.
Upload the project files, but do not upload `.venv/`, `db.sqlite3`, or `__pycache__/`.
Then include the GitHub repository link in your internship submission and project video.

## 5. Project structure
```text
CodeAlpha_Ecommerce_Store/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── store/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── cart.py
│   ├── forms.py
│   ├── tests.py
│   ├── migrations/
│   │   └── __init__.py
│   └── management/
│       └── commands/
│           └── seed_products.py
└── templates/
    ├── base.html
    ├── registration/
    │   └── login.html
    └── store/
        ├── home.html
        ├── product_detail.html
        ├── cart.html
        ├── checkout.html
        ├── order_success.html
        └── my_orders.html
```
