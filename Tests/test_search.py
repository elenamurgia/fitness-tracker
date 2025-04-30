import pytest
import requests
from unittest.mock import patch, Mock
from CLI.client_side import ExerciseSearchDB
from CLI.client_side import ExerciseSearchAPI

#test: user enters normal string: should return lowercase, stripped string
@patch('builtins.input', return_value= '  Chest  ')
def test_get_muscle_from_user(mock_input):
    instance = ExerciseSearchAPI("https://testserver")
    result = instance.get_muscle_from_user()
    assert result == 'chest'

@patch('requests.get') # mocks requests.get
def test_get_exercise_api(mock_get):
    mock_response_data = [{"Name: Close-grip bench press", "Type: strength", "Equipment needed: barbell",
"difficulty: intermediate", "instructions: instructions"}]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_data
    mock_get.return_value = mock_response

    instance = ExerciseSearchAPI("http://testserver")
    instance.url = "https://api.example.com/exercises"
    instance.api_key = "test_key"

    muscle = "chest"
    response = instance.get_exercise_api(muscle)

    expected_url = "https://api.example.com/exercises?muscle=chest"
    mock_get.assert_called_once_with(expected_url,headers={'X-Api-Key': 'test_key'})

    assert response.status_code ==200
    assert response.json() == mock_response_data

#test: user enters normal string: should return lowercase, stripped string
@patch('builtins.input', return_value= '  Chest  ')
def test_get_muscle_from_user_db(mock_input):
    search = ExerciseSearchDB("https://testserver")
    result = search.get_muscle_from_user_db()
    assert result == 'chest'

@patch('requests.get') # mocks requests.get
def test_get_exercises_muscle_db(mock_get):
    mock_response_data = [{"Name: Close-grip bench press", "Type: strength", "Equipment needed: barbell",
                           "difficulty: intermediate", "instructions: instructions"}]
    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_get.return_value = mock_response

    search = ExerciseSearchDB("http://testserver")
    result = search.get_exercises_muscle_db("chest")
    assert result == mock_response_data
    mock_get.assert_called_with("http://testserver/user_exercises", params={'muscle': 'chest'})


#Amber's code
# def test_user_exercises_missing_param(client):
#     response = client.get('/user_exercises')
#     assert response.status_code == 400
#     assert response.json == {"error": "Missing muscle parameter"}
#
# @patch('app.exercise_db.get_exercise_db')
# def test_user_exercises_with_valid_param(mock_get_exercise_db, client):
#     mock_get_exercise_db.return_value = [{"name": "Push-up", "muscle": "chest"}]
#     response = client.get('/user_exercises?muscle=chest')
#     assert response.status_code == 200
#     assert response.json == [{"name": "Push-up", "muscle": "chest"}]



