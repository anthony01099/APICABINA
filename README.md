# ApiCabina
API for managing a biosecurity system


### API Description

- POST {"username":"username", "password": "password"}  /api/auth/login/  -> Login with credentials
- GET /api/auth/logout/  -> Logout from current session
- GET /api/auth/ -> Get all system's users
- GET /api/auth/user_id/ -> Get user info


### Data Base Entity Relationship Diagram
![ERD](./docs/api_cabina_erd.png)

### Run tests

...

### Run development server
    python manage.py runserver 80

### Seed database with test data
    python manage.py seed
Test user: test. Password: test_password
