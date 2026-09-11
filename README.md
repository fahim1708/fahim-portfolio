# Personal Portfolio

Production-ready Django foundation for Md. Naimuzzaman Fahim's personal portfolio.

## Stack

- Python 3.10+
- Django
- Django Templates
- SQLite for local development
- PostgreSQL for production

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Run migrations:

```powershell
python manage.py migrate
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver
```

The site will be available at `http://127.0.0.1:8000/` and Django Admin at `http://127.0.0.1:8000/admin/`.

## Environment Variables

- `DJANGO_SECRET_KEY`: required secret key for Django.
- `DJANGO_DEBUG`: use `True` locally and `False` in production.
- `DJANGO_ALLOWED_HOSTS`: comma-separated allowed hosts.
- `RENDER_EXTERNAL_HOSTNAME`: Render-provided hostname, such as `portfolio.onrender.com`.
- `VERCEL_URL`, `VERCEL_BRANCH_URL`, and `VERCEL_PROJECT_PRODUCTION_URL`: Vercel-provided hostnames used automatically for allowed hosts and CSRF origins.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated HTTPS origins when additional trusted origins are needed.
- `DATABASE_URL`: leave blank for local SQLite; set to a PostgreSQL URL in production.
- `CLOUDINARY_CLOUD_NAME`: Cloudinary cloud name for production media storage.
- `CLOUDINARY_API_KEY`: Cloudinary API key for production media storage.
- `CLOUDINARY_API_SECRET`: Cloudinary API secret for production media storage.
- `DJANGO_SECURE_SSL_REDIRECT`: enables HTTPS redirect when `DJANGO_DEBUG=False`.
- `DJANGO_SECURE_HSTS_SECONDS`: HSTS duration for production.
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`: include subdomains in HSTS.
- `DJANGO_SECURE_HSTS_PRELOAD`: enable HSTS preload.

## Production Notes

Set `DJANGO_DEBUG=False`, provide a strong `DJANGO_SECRET_KEY`, configure `DJANGO_ALLOWED_HOSTS`, and set `DATABASE_URL` to your PostgreSQL connection string. Configure the three Cloudinary variables for persistent admin-uploaded media. Static files are collected into `staticfiles/` and served by WhiteNoise; media files are stored separately in Cloudinary. Render can use the included `render.yaml` build and start commands. Vercel uses `api/index.py` as its Python serverless entry point and the included `vercel.json` for routing; run `python manage.py migrate` against the production database before using the admin.
