#!/bin/sh
echo "Apply migrations, cerate super user and collectstatic"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --email test@test.com --noinput
python manage.py collectstatic --noinput


echo "Start gunicorn server"
gunicorn -c config/gunicorn.py
celery -A config -b "amqp://rabbitmq:5672/vhost" beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
exec "$@"
