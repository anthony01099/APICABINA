FROM python:3.7-buster

WORKDIR /usr/src/app

RUN pip install gunicorn

RUN pip install daphne

RUN  pip install psycopg2

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD rm -rf static/* && \
    python manage.py collectstatic && \
    python manage.py migrate  &&  \
    python manage.py seed_user  &&  \
    gunicorn --workers 5 --bind  0.0.0.0:8000  api_cabina.wsgi:application --log-level=info --log-file /var/log/gunicorn.log
