web: gunicorn config.wsgi -c gunicorn.conf.py
release: python manage.py migrate && python manage.py load_sample_data

