from unittest.mock import patch, Mock
from CLI.client_side import ExerciseSearchDB
from CLI.client_side import ExerciseSearchAPI


#Test: user enters normal string: should return lowercase, stripped string
@patch('builtins.input', return_value= '  Chest  ')
def test_get_muscle_from_user(mock_input):
    instance = ExerciseSearchAPI("https://testserver")
    result = instance.get_muscle_from_user()
    assert result == 'chest'

#Test that function get_exercise_api correctly sends a GET request and returns the expected mock response from the API
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

#Test: user enters normal string: should return lowercase, stripped string
@patch('builtins.input', return_value= '  Chest  ')
def test_get_muscle_from_user_db(mock_input):
    search = ExerciseSearchDB("https://testserver")
    result = search.get_muscle_from_user_db()
    assert result == 'chest'

#Test that function get_exercises_muscle_db correctly sends a GET request and returns the expected mock response
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

#Test that function get_exercises_muscle_db handles errors
@patch('requests.get') # mocks requests.get
def test_get_exercises_muscle_db_incorrect_response(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {} #simulates an empty response (no exercises found)

    mock_get.return_value = mock_response

    search = ExerciseSearchDB("http://testserver")

    result = search.get_exercises_muscle_db("chest")

    assert result == {} #It should return an empty dictionary
    mock_get.assert_called_with("http://testserver/user_exercises", params={'muscle': 'chest'})
