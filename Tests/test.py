import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the CFG Fitness App' in response.data

def test_favicon_route(client):
    response = client.get('/favicon.ico')
    # It will return 200 if favicon.ico is found in /static; otherwise 404
    assert response.status_code in (200, 404)

def test_user_exercises_missing_param(client):
    response = client.get('/user_exercises')
    assert response.status_code == 400
    assert response.json == {"error": "Missing muscle parameter"}

@patch('app.exercise_db.get_exercise_db')
def test_user_exercises_with_valid_param(mock_get_exercise_db, client):
    mock_get_exercise_db.return_value = [{"name": "Push-up", "muscle": "chest"}]
    response = client.get('/user_exercises?muscle=chest')
    assert response.status_code == 200
    assert response.json == [{"name": "Push-up", "muscle": "chest"}]

@patch('app.conn.cursor')
def test_get_user_workouts_user_not_found(mock_cursor_factory, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_cursor_factory.return_value = mock_cursor

    response = client.get('/testuser/workouts')
    assert response.status_code == 404
    assert b"User 'testuser' not found" in response.data

@patch('app.conn.cursor')
def test_post_workout_missing_fields(mock_cursor_factory, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [1]  # User ID found
    mock_cursor_factory.return_value = mock_cursor

    response = client.post('/testuser/workouts', json={})
    assert response.status_code == 400
    assert response.json == {"error": "exercise_id and duration_minutes are required"}


