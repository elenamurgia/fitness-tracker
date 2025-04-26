import pytest
from API.fitness_api import app

@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True
    })
    return app.test_client()

# Test mock data
test_user = "test_user"
test_user_id = 1
test_exercise_id = 1

# Test fetching workouts for a user that doesn't exist
def test_get_user_workouts_user_not_found(client):
    response = client.get("/non_existent_user/workouts")
    assert response.status_code == 404
    assert b"User 'non_existent_user' not found" in response.data


# Test log workouts with missing parameters
def test_log_user_workout_missing_parameters(client):
    response = client.post(
        "/test_user/workouts",
        json={
            "exercise_id": None,
            "duration_minutes": None,
        }
    )
    assert response.status_code == 404



