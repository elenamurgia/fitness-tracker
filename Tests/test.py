import unittest
from unittest import mock
from CLI.client_side import ExerciseSearchAPI


#-----Paula's Code-----
class GetMuscleFromUserTest(unittest.TestCase):
    @mock.patch('APP.client_side.input', create=True)
    def test_get_muscle_from_user(self, mocked_input):
        mocked_input.return_value = (' BicePs  ')
        obj = ExerciseSearchAPI(api_key='fake_api_key')
        result = obj.get_muscle_from_user()
        self.assertEqual(result, 'biceps')

if __name__ == "__main__":
    unittest.main()
