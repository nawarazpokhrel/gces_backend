web: gunicorn gces_backend.wsgi --log-file -
python manage.py collectstatic --noinput
manage.py migrate