FROM python:3.7-buster

WORKDIR /usr/src/app

RUN pip install gunicorn

RUN pip install daphne

RUN  pip install psycopg2

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD python manage.py migrate&&gunicorn --workers 5 --bind  0.0.0.0:8000  api_cabina.wsgi:application --log-file /var/log/gunicorn.log&&daphne -u /tmp/daphne.sock -b 0.0.0.0 -p 8001 api_cabina.asgi:application
