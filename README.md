# Trackerr v1.1 Backend

A Django-based backend for the Trackerr application, handling APIs, Celery tasks, and real-time channels.

---

## Important Dependency

Before installing the Python requirements, make sure to install the following system packages:

```bash
sudo apt install -y libpq-dev gcc python3-dev
```

## Clone the repository

```bash
git clone <your-repo-url>
cd trackerr_v1/

## Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate

## Install dependencies
```bash
pip install -r requirements.txt


## Add all environmental variables with the keys below
SECRET_KEY
POSTGRES_HOST
PASSWORD
DEBUG
EMAIL
EMAIL_PASSWORD
CELERY_BROKER_URL
CELERY_RESULT_BACKEND
CELERY_TIMEZONE
CELERY_ENABLE_UTC
CELERY_ACCEPT_CONTENT
CELERY_TASK_SERIALIZER
CHANNEL_REDIS_HOST
CHANNEL_REDIS_PORT
DOCUMENTATION_URL
AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID
ACCOUNT_ID
TRACKERR_CDN_URL

## Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate

## Start the server
# Start Django development server
python manage.py runserver 0.0.0.0:8000

# Start Celery worker
```bash 
celery -A trackerr_v1 worker --concurrency=1 --loglevel=INFO

# Start Celery Beat for periodic tasks
```bash
celery -A trackerr_v1 beat --loglevel=INFO

## Notes

- Ensure Postgres and Redis are running before starting the app.

- Use Nginx as a reverse proxy in production for better performance and SSL termination.
