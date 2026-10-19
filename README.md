# Productivity Tool — Flask Backend

## Overview

This project is a Flask backend for a productivity application. It allows users to create accounts, log in, and manage their personal notes. Flask sessions are used for authentication, and users can only access notes that belong to them.

## Technologies Used

- Python 3.8
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite
- Marshmallow
- Faker
- Pytest

## Setup and Installation

1. Clone the repository.
2. Install Pipenv if it is not already installed.
3. Install the project dependencies:

   ```bash
   pipenv install
   ```

4. Apply the database migrations:

   ```bash
   pipenv run flask --app app db upgrade
   ```

5. Add a secure `SECRET_KEY` environment variable before running the application outside local development.

## Running the Application

Start the Flask server:

```bash
pipenv run python app.py
```

The backend runs at `http://127.0.0.1:5555`.

## Database and Seed Data

To create sample users and notes, run:

```bash
pipenv run python -c 'import seed'
```

**Warning:** The seed script resets the local database. Use it only when you are comfortable deleting existing local data.

Development seed accounts:

- Username: `imaan`
- Password: `Password123!`
- Username: `amina`
- Password: `Password123!`

These credentials are for local development only.

## Authentication Endpoints

| Method | Endpoint         | Description               |
| ------ | ---------------- | ------------------------- |
| POST   | `/signup`        | Register a user           |
| POST   | `/login`         | Log in                    |
| GET    | `/check_session` | Check the current session |
| DELETE | `/logout`        | Log out                   |

Signup accepts `username`, `password`, and `password_confirmation`. Login accepts `username` and `password`.

## Notes Endpoints

All Notes endpoints require an authenticated session.

| Method | Endpoint      | Description                     |
| ------ | ------------- | ------------------------------- |
| GET    | `/notes`      | List the logged-in user's notes |
| POST   | `/notes`      | Create a note                   |
| GET    | `/notes/<id>` | Retrieve a note                 |
| PATCH  | `/notes/<id>` | Update a note                   |
| DELETE | `/notes/<id>` | Delete a note                   |

### Pagination

Notes can be paginated using query parameters:

```text
GET /notes?page=1&per_page=10
```

The response includes the notes and pagination information. The maximum page size is 100 notes.

## Security and Validation

- Passwords are stored as hashes using Flask-Bcrypt.
- Usernames must be unique.
- Login requires valid credentials.
- Notes routes require an authenticated session.
- Users cannot access, update, or delete another user's notes.
- Invalid note fields and pagination values are rejected.

## Database Migrations

To generate a migration after changing a model:

```bash
pipenv run flask --app app db migrate -m "Describe your changes"
pipenv run flask --app app db upgrade
```

## Development Notes

This project is intended for learning and local development. Before production deployment, configure a secure secret key, disable debug mode, and use appropriate production security settings.
