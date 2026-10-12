# TaskPro

Personal task manager. Django + DRF + MySQL backend with JWT auth, and a Bootstrap + Fetch API frontend served by Django. Each user only sees their own tasks.

## Run

1. Create the database in MySQL:
   ```sql
   CREATE DATABASE taskpro CHARACTER SET utf8mb4;
   ```
2. Set your MySQL password in `config/settings.py` (`YOUR_MYSQL_PASSWORD`) or via env vars `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
3. Install and start:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
4. Open http://127.0.0.1:8000/ and register.

## Test

```bash
python manage.py test
```
(No MySQL available? Run with `USE_SQLITE=1` set.)

## API

| Method | URL | Description |
|---|---|---|
| POST | /api/register/ | register |
| POST | /api/login/ | get JWT access token |
| GET | /api/tasks/ | list (`?status=pending\|completed`, `?priority=`, `?search=`), sorted by due date ascending |
| POST | /api/tasks/ | create |
| PUT/PATCH | /api/tasks/<id>/ | edit / mark complete |
| DELETE | /api/tasks/<id>/ | delete |

Send the token as `Authorization: Bearer <access>`.

## Structure

```
config/        settings, root urls
tasks/         model, serializers, views, urls, tests
templates/     login.html, dashboard.html (Bootstrap + Fetch)
```

## Tech

Python, Django, Django REST Framework, SimpleJWT, MySQL, Bootstrap 5
