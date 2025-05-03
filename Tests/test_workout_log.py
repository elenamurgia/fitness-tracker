import pytest
import random
from API.fitness_api import app

# Creates a test client for the Flask app.
@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True
    })
    return app.test_client()

# Helper function to make sure a user exists before running the tests.
def ensure_user_exists(username):
    conn = app.config['db_connection']
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (username, user_password) VALUES (%s, %s)", (username, 'test123'))
        conn.commit()
    cursor.close()


# Test fetching workouts for an existing user
def test_get_workouts_existing_user(client):
    ensure_user_exists("tester")
    response = client.get("/tester/workouts")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test fetching workouts for a user that doesn't exist
def test_get_workouts_non_existent_user(client):
    response = client.get("/non_existent_user/workouts")
    assert response.status_code == 404
    assert b"User 'non_existent_user' not found" in response.data

# Test fetching workouts for a user with no workouts
def test_get_workouts_empty_user(client):
    ensure_user_exists("empty_user")
    response = client.get("/empty_user/workouts")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

# Test logging a workout successfully
def test_log_user_workout_success(client):
    ensure_user_exists("tester")
    payload = {
        "exercise_id": 1,
        "duration_minutes": 30,
        "notes": "Felt great!"
    }
    response = client.post("/tester/workouts", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Workout logged successfully!"

# Test logging a workout with missing parameters
def test_log_workout_missing_parameters(client):
    ensure_user_exists("tester")
    payload = {
        "exercise_id": None,
        "duration_minutes": None,
    }
    response = client.post("/tester/workouts", json=payload)
    assert response.status_code in (400, 404)

# Test logging a workout for a user that doesn't exist
def test_log_workout_nonexistent_user(client):
    payload = {
        "exercise_id": 1,
        "duration_minutes": 20,
        "notes": "Another session!"
    }
    response = client.post("/non_existent_user/workouts", json=payload)
    assert response.status_code == 404

# Test logging a workout with additional fields
def test_log_workout_with_extra_fields(client):
    ensure_user_exists("tester")
    payload = {
        "exercise_id": 1,
        "duration_minutes": 20,
        "notes": "Extra field test",
        "unexpected_field": "ignored"
    }
    response = client.post("/tester/workouts", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Workout logged successfully!"

# Test fetching sets for an existing workout
def test_get_sets_existing_workout(client):
    ensure_user_exists("tester")
    response = client.get("/tester/1/sets")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

# Test fetching sets for a workout that has no sets
def test_get_sets_no_sets_found(client):
    ensure_user_exists("tester")
    response = client.get("/tester/445678999/sets")
    assert response.status_code == 404
    assert b"No sets found" in response.data

# Test fetching sets for a user that doesn't exist
def test_get_sets_user_not_found(client):
    response = client.get("/non_existent_user/1/sets")
    assert response.status_code == 404
    assert b"User 'non_existent_user' not found" in response.data

# Test posting a valid exercise set
def test_post_set_success(client):
    ensure_user_exists("tester")
    set_number = random.randint(1000, 1999)
    payload = {
        "set_number": set_number,
        "reps": 15,
        "weight": 50.0,
        "distance_km": None,
        "duration_seconds": 60,
        "rest_seconds": 90
    }
    response = client.post("/tester/1/sets", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Set logged successfully!"

# Test posting a set with missing required fields (in this case set_number)
def test_post_set_missing_set_number(client):
    ensure_user_exists("tester")
    payload = {
        "reps": 10,
        "weight": 40.0,
        "duration_seconds": 45,
        "rest_seconds": 60
    }
    response = client.post("/tester/1/sets", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

# Test posting a set for a user that doesn't exist
def test_post_set_user_not_found(client):
    payload = {
        "set_number": 1,
        "reps": 12,
        "weight": 35.0,
        "distance_km": None,
        "duration_seconds": 50,
        "rest_seconds": 30
    }
    response = client.post("/non_existent_user/1/sets", json=payload)
    assert response.status_code == 404
    assert b"User 'non_existent_user' not found" in response.data
