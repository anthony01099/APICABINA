# ApiCabina
API for managing a biosecurity system


### API Description

- POST {"username":"username", "password": "password"}  /api/auth/login/  -> Login with credentials
- GET /api/auth/logout/  -> Logout from current session
- GET /api/auth/ -> Get all system's users
- GET /api/auth/user_id/ -> Get user info
- GET /api/data/company -> Get all system's companies
- GET /api/data/company/company_id/ -> Get companies info
- GET /api/data/captures -> Get all system's captures
- GET /api/data/captures/capture_id/ -> Get capture info
- GET /api/data/cabins_company/company_id/ -> Get cabins for a company
- GET /api/data/captures_company/company_id/ -> Get captures for a company
- GET /api/data/captures_cabin/cabin_id/ -> Get captures for a cabin

### Data Base Entity Relationship Diagram
![ERD](./docs/api_cabina_erd.png)

### Run tests

...

### Run development server
    python manage.py runserver 80

### Seed database with test data
    python manage.py seed
Test user: test. Password: test_password
