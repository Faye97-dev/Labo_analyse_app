release: python manage.py migrate && python manage.py app_init
web: gunicorn demo_sante.wsgi --log-file -