# Tournament Arena

Tournament Arena is a Django web application for organizing tournaments, teams, and player rosters with social authentication and user profiles.

## Features
- Tournaments: create, edit, and delete tournaments with name, location, description, date, and banner upload; ordered lists, a cached listing per user (30s), and a paginated view (3 per page) with registration counters for signed-in users.
- Teams and players: create teams with emblems bound to a tournament, edit/delete them with permission checks, join or leave teams as a user, keep rosters unique per user-team pair, and add players manually when you have roster permissions.
- Registrations: add multiple slots for yourself to a tournament, see a personal registrations summary with totals, and decrease or remove registrations in a couple of clicks.
- Accounts and profiles: sign up with captcha, log in/log out, reset or change passwords, use one-click Google login via django-allauth, and maintain a profile with display name, bio, and avatar uploads plus on-screen success/error messaging.
- UI and storage: Django Templates with Bootstrap-style forms, media uploads stored under `media/`, and lightweight caching to keep the tournament pages quick.

## Tech stack
- Django 5.2, Python 3.11+, MySQL (via `ENGINE/NAME/USER/PASSWORD/HOST/PORT`).
- Auth and security: django-allauth (Google provider), django.contrib.auth, captcha.
- Config: `pydantic-settings` loads `.env` via `config.py`.
- Media: Pillow-backed file uploads for banners, emblems, and avatars.
- Runtime: `LocMemCache` for fast list rendering; ready for gunicorn-based deployments.

## Project layout
```
.
├── manage.py
├── config.py
├── GamesTournaments/   # tournaments, teams, registrations
├── UserManager/        # auth, profiles, social login
├── templates/          # Django templates
├── media/              # uploaded files (gitignored)
├── requirements.txt
└── .env                # local secrets and database settings
```

## Setup (local)
1) Create a virtual environment and install dependencies:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
2) Create `.env` in the project root:
```
ENGINE=django.db.backends.mysql
NAME=tournaments_db
USER=tournaments_user
PASSWORD=your_password
HOST=localhost
PORT=3306
SECRET_KEY=django-insecure-change-me
```
3) Apply migrations and create an admin:
```
python manage.py migrate
python manage.py createsuperuser
```
4) Run the server:
```
python manage.py runserver
```
5) (Optional) Configure Google OAuth in `/admin/socialaccount/socialapp/`, then test social login.

## Common commands
- `python manage.py collectstatic --noinput` — gather static assets for deployment.
- `python manage.py test` — run the Django test suite.
- `python manage.py changepassword <username>` — rotate a password from CLI.
- `python manage.py shell` — assign `manage_tournaments`, `manage_teams`, or `manage_roster` permissions/groups programmatically.

## Useful notes
- Tournament lists are cached per user for 30 seconds; editing a tournament/team clears cache so updates appear instantly.
- Media uploads live in `media/`; keep the directory writable locally and map it to persistent storage in production.
- The email backend is console-only in development, so wire up SMTP before relying on password resets in production.
