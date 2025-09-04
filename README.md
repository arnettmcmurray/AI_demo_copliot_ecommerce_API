# E-Commerce API

A full-featured e-commerce API built with Flask, engineered for production-level quality.

## Features
- User registration, login, update, delete (JWT auth, hashed passwords).
- Role-based access (Admins manage products, users manage carts/orders).
- Product CRUD with stock tracking and categories.
- Cart staging and checkout flow → creates orders with items and total price.
- Swagger UI at `/apidocs` with live docs and examples.
- Full unit test suite (users, products, carts, orders).
- Seed script to bootstrap admin, user, and sample products.
- SQLite for dev, Postgres ready for production (Render/Heroku).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
python seed.py
flask run
```

## Testing
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Deployment
- Procfile included for Render/Heroku.
- `.env.example` provided for environment variables.

## Author
Arnett McMurray — built to flex on Dylan 😎
