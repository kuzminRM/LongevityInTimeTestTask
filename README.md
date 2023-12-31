# LongevityInTimeTestTask

## How to set up the project (dev)
1. Clone GIT repo `git clone https://github.com/kuzminRM/LongevityInTimeTestTask.git`
2. Enter in project root
3. Create `.env` file with the following contents:
```
DJANGO_SECRET_KEY=django-secret-key
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=127.0.0.1 localhost

MYSQL_NAME=db_name
MYSQL_USER=user
MYSQL_PASSWORD=pass
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306

CELERY_BROKER_URL=amqp://login:pass@localhost

EMAIL_HOST_USER=my@email.com
EMAIL_HOST_PASSWORD=email_pass

RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=pass
```
3. Create python 3.10 virtual environment `python -m venv venv` and activate it `source venv/bin/activate`
4. Load python packages `pip install -r requirements.txt` (you may need to install additional system packages)
5. Setup MySQL DB
6. Setup some broker for Celery with AMQP support (e.g. RabbitMQ)
7. Run migrations on DB `python manage.py migrate`
8. Run Celery worker `celery -A LongevityInTimeTestTask worker -l INFO`
9. Run test server `python manage.py runserver 0.0.0.0:8000`

## How to deploy
1. Repeat steps 1-3 from dev setup instruction exept for `.env` file should be named as `.env.prod`
2. Run `sudo docker compose build` (or `docker-compose` for older versions)
3. Run `sudo docker compose up -d` (or perform similar actions to run the project on bare hardware)
