# Md. Naimuzzaman Fahim | Portfolio

A professional portfolio website built with Django to showcase a software engineer's profile, projects, research, experience, skills, and contact information in a polished and maintainable way.

## What is this project?

This project is a personal portfolio platform for Md. Naimuzzaman Fahim. It serves as a digital professional identity and hiring hub where visitors can:

- learn about the developer's background and expertise
- explore featured work and technical projects
- review education, certifications, and career experience
- browse research and technical writing
- contact the developer directly through a form

The site is designed to look modern, credible, and professional while keeping content easy to manage from the Django admin panel.

## What is the project outcome/result?

The outcome is a fully functional, production-ready portfolio website that acts as a personal brand presence online. It helps the owner:

- present skills and experience in a structured format
- highlight impactful projects and research
- increase visibility to recruiters, clients, and collaborators
- collect messages and engagement through a contact form
- update content without needing to change code manually

In short, the result is a scalable portfolio that turns technical work into a clear, professional digital presence.

## How is it done?

This project is built using Django, Python, and a modular app structure.

### Core architecture

- `apps.core` manages the main portfolio content such as profile, about section, skills, social links, and resume
- `apps.projects` handles project listings, published work, technologies, thumbnails, and detail pages
- `apps.research` stores research and technical content with featured and detail views
- `apps.experience` manages professional experience, education, and certifications
- `apps.contact` handles contact information and message submissions

### Frontend and UX

- Django Templates are used to render the site
- static CSS and JS assets are organized under `static/`
- media such as profile images, project assets, and resumes are supported through the media setup
- responsive presentation is used to keep the portfolio readable across devices

### Content management

The site is not just a static landing page. It is built as a content-driven CMS-style portfolio, where the site owner can manage information through Django admin. Important content is stored as models, including:

- personal profile and headline
- about items and skill categories
- featured projects and technologies
- research items
- certifications and experience entries
- contact details

### Deployment and environment setup

The project supports both local development and production environments:

- SQLite is used by default for local work
- PostgreSQL can be configured in production through `DATABASE_URL`
- Cloudinary is used for persistent media storage when enabled
- WhiteNoise is configured for static file delivery in production
- deployment is compatible with hosting platforms such as Render and Vercel

## Tech stack

- Python 3.10+
- Django
- Django Templates
- SQLite for local development
- PostgreSQL for production
- Cloudinary for media storage
- WhiteNoise for static files

## Features

- Professional home page with personal profile and hero content
- About section with structured portfolio details
- Skills grouped into categories
- Experience, education, and certification timeline
- Featured and detailed project pages
- Research section with publishable entries
- Resume management
- Contact form for user inquiries
- SEO-friendly pages including sitemap and robots.txt support

## Local setup

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

## Environment variables

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

## Production notes

Set `DJANGO_DEBUG=False`, provide a strong `DJANGO_SECRET_KEY`, configure `DJANGO_ALLOWED_HOSTS`, and set `DATABASE_URL` to your PostgreSQL connection string. Configure the three Cloudinary variables for persistent admin-uploaded media. Static files are collected into `staticfiles/` and served by WhiteNoise; media files are stored separately in Cloudinary. Render can use the included `render.yaml` build and start commands. Vercel uses `api/index.py` as its Python serverless entry point and the included `vercel.json` for routing; run `python manage.py migrate` against the production database before using the admin.

## Summary

This portfolio project combines a clean personal brand design with a strong Django backend, making it easy to maintain and scale. It delivers a modern online identity that can represent a developer professionally, attract opportunities, and keep portfolio content manageable through Django admin.
