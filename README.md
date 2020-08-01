# ApiCabina
API for managing a biosecurity system


### API Description

- POST {"username":"username", "password": "password"}  /api/auth/login/  -> Login with credentials
- GET /api/auth/logout/  -> Logout from current session
- GET /api/auth/ -> Get all system's users
- GET /api/auth/user_id/ -> Get user info
