web: gunicorn config.wsgi -c gunicorn.conf.py
release: python manage.py clean_database && python manage.py migrate --run-syncdb && python manage.py load_educational_data

