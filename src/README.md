# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- See signed-up participants on each activity card, updated after sign-up or removal
- Sign up for activities
- Unregister a participant using the trash icon next to their email

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Unregister a participant; returns 404 if the activity or registration does not exist |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Testing

From the repository root, install the development dependencies and run the tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

Tests live in the separate `tests/` directory and follow the
Arrange-Act-Assert (AAA) pattern. Shared pytest fixtures provide isolated activity
data for every test and restore the application's original data afterward.
FastAPI's TestClient exercises the API and static routes without a running server
or external services.

Run `python -m pytest -q` to use the configured test discovery.
