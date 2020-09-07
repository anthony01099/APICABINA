# ApiCabina
API for managing a biosecurity system

### API Description

- POST [username,password]  /api/auth/login/  --> Login with credentials. Perm: (any).
- GET /api/auth/logout/  --> Logout from current session. Perm: (auth).
- GET /api/auth/ --> Get all system's users. Perm: (super user).
- GET /api/auth/user_id/ --> Get user info. Perm: (super user).
- GET /api/data/company --> Get all system's companies. Perm: (super user).
- GET /api/data/company/company_id/ --> Get companies info. Perm: (super user).
- GET /api/data/company_data/ --> Get company info from current user. Perm: (auth).
- GET /api/data/cabins_company/ --> Get cabins for a company. Perm: (auth).
- GET /api/data/captures_company/capture_id --> Get a specified capture by id. Perm: (auth).
- GET /api/data/captures_company/ --> Get captures for a company. Perm: (auth).
- GET /api/data/captures_cabin/cabin_id/ --> Get captures for a cabin. Perm: (auth).
- GET /api/data/captures --> Get all system's captures. Perm: (super user).
- GET /api/data/captures/capture_id/ --> Get capture info. Perm: (super user).
- POST [token,temp,is_wearing_mask,is_image_saved,image_base64]  /api/data/captures_create/ --> Create a capture. Perm: (any).
- POST [token]  /api/data/register_cabin/ --> Register cabin. Perm: (auth).
- POST [token]  /api/data/associate_token/ --> Assoc Token for notifications. Perm: (auth).
- POST [token]  /api/data/delete_token/ --> Delete Token. Perm: (auth).
### Web interface for admin

- Management: /admin/
- QR code generator: /web/create_token/

### Notification system
A simple notification system for alerts is implemented through django-channels (ASGI). For listing to notification follow the instructions:

- Authenticate an user related to a company.
- Start a websocket conection to ws://server-domain/ws/alerts/. The following cookies must be provided for the server to accept the conection: csrftoken, sessionid (use this key names).
- Listen for incoming messages. They will provide the following keys with their values: capture_id, is_wearing_mask, temp.

For production use, a redis server must be provided for interprocess communication.

### Run tests
    python manage.py test

### Run development server
    python manage.py runserver 80

### Seed database with test data
    python manage.py seed
Test user: test1. Password: test_password

## Data Base Entity Relationship Diagram
![ERD](./docs/api_cabina_erd.png)

## User admin
To create an admin user for a company:

1-Create the user.</br>
2-Add the user to the "Company admin" group.</br>
3-Mark the user as "Staff User".</br>
4-Create a new Client object with the user and the company.</br>


## Deploy

To deploy this service:

1-Log into the server.<br>
2-Clone the repository with git clone git@github.com:jesuscol96/ApiCabina.git.<br>
3-run : sudo docker-compose up -d <br>

### To run commands inside the application container.
1-sudo docker container exec -it api_cabina bash.<br>
2-Run your command.<br>

### To run commands inside the database container.
1-sudo docker container exec -it postgres bash.<br>
2- Run your commands here.<br>

### To update the code

1- sudo docker-compose down.<br>
2- Backup the media directory.<br>
3- cd ..<br>
4- rm -rf ApiCabina.<br>
5- git clone git@github.com:jesuscol96/ApiCabina.git.<br>
6- cd ApuCabina.<br>
7- docker-compose up -d.


### Update script
Run the update script in the folder api-cabina as root user.
sudo ./update_code.sh

#!/bin/bash

export PATH="/snap/bin/:$PATH"

cd ApiCabina

docker-compose down

cd ..

rm -Rf ApiCabina

git clone git@github.com:jesuscol96/ApiCabina.git

cd  ApiCabina

docker-compose up -d
