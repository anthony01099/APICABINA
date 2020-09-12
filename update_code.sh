#!/bin/bash

export PATH="/snap/bin/:$PATH"

cd ApiCabina

docker-compose down

cd ..

rm -Rf ApiCabina

git clone git@github.com:jesuscol96/ApiCabina.git

cd  ApiCabina

docker-compose up -d

docker container exec api_cabina python manage.py collectstatic --no-input
