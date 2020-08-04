# ApiCabina
API for managing a biosecurity system


### API Description

- POST [username,password]  /api/auth/login/  --> Login with credentials
- GET /api/auth/logout/  --> Logout from current session
- GET /api/auth/ --> Get all system's users
- GET /api/auth/user_id/ --> Get user info
- GET /api/data/company --> Get all system's companies
- GET /api/data/company/company_id/ --> Get companies info
- GET /api/data/cabins_company/ --> Get cabins for a company
- GET /api/data/captures_company/ --> Get captures for a company
- GET /api/data/captures_cabin/cabin_id/ --> Get captures for a cabin
- GET /api/data/captures --> Get all system's captures
- GET /api/data/captures/capture_id/ --> Get capture info
- POST [cabin_id,temp,is_wearing_mask,is_image_saved,image_base64]  /api/data/captures_create/ --> Create a capture.

### Data Base Entity Relationship Diagram
![ERD](./docs/api_cabina_erd.png)

### Run tests

...

### Run development server
    python manage.py runserver 80

### Seed database with test data
    python manage.py seed
Test user: test1. Password: test_password
