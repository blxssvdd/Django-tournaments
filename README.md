# Tournament Arena

Веб-приложение на Django для управления турнирами, командами и игроками

## Возможности
- Каталог турниров с пагинацией и списком избранных событий.
- Регистрация, вход, сброс пароля и защищённый CRUD.
- Адаптивный интерфейс на Django Templates и Bootstrap 5.
- Хранение конфигурации и секретов через переменные окружения.

## Стек
- Backend: Django 5, Whitenoise, Pydantic Settings, Gunicorn.
- База данных: MySQL (поддерживается `DATABASE_URL`).
- Frontend: Django Templates, Bootstrap, кастомные CSS/JS.
- Инфраструктура: Railway + Procfile.

## Быстрый старт
```bash
git clone https://github.com/you/django-tournament.git
cd django-tournament
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
cp Tournaments/.env.example Tournaments/.env
python Tournaments/manage.py migrate
python Tournaments/manage.py createsuperuser
python Tournaments/manage.py runserver
```

## Переменные окружения (`Tournaments/.env`)
```ini
DJANGO_SECRET_KEY=
DATABASE_URL=
ENGINE=
NAME=
USER=
PASSWORD=
HOST=
PORT=
```

## Полезные команды
- python manage.py migrate — применить миграции.
- python manage.py collectstatic --noinput — собрать статику.
- python manage.py test — запустить тесты.
- gunicorn Tournaments.wsgi --bind 0.0.0.0:${PORT} — продакшн-сервер.

