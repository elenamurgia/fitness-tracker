from AUTH.auth import UserAuth
import requests
import random
from DB.workout_log import WorkoutLog
from config import API_KEY


def main_menu(cursor, conn):
    auth = UserAuth(cursor, conn)

    while True:
        print("\nWelcome to the CFG Fitness App")
        print("Select a number to choose an option:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user_id = auth.login()
            if user_id:
                logged_in_menu(cursor, conn, user_id)
        elif choice == "2":
            auth.register()
        elif choice == "3":
            print("Buh-byeeee!")
            break
        else:
            print("Invalid input. Try again.")

# Elena's code
# Menu available after the user has logged in
def logged_in_menu(cursor, conn, user_id):
    # Create an instance of the workout log
    workout_log = WorkoutLog(cursor, conn)
    while True:
        print("\nLogged in")
        print("\nMAIN MENU")
        print("Select a number to choose an option:")
        print("1. View Workout Menu")
        print("2. Browse by Category (arms, legs, chest, etc.)")
        print("3. Logout")
        choice = input(">> ")

        if choice == "1":
            print("\nWORKOUT MENU")
            print("1. View Past Workouts")
            print("2. Log New Workout")
            print("3. View Progress")
            print("4. View Favourites")
            print("5. Go back to the Main Menu")
            print("6. Logout")
            choice_workout_menu = input(">> ")
            if choice_workout_menu == "1":
                # Display previously logged workouts
                workouts = workout_log.view_all_logged_workouts(user_id)
                if workouts:
                    print("\nYour workout Log:")
                    for w in workouts:
                        workout_log_id = w[0]
                        print(f"Log ID: {w[0]}")
                        print(f"Exercise: {w[1]}")
                        print(f"Duration: {w[2]} minutes")
                        print(f"Notes: {w[3]}")
                        formatted_date = w[4].strftime("%-d %B %Y at %H:%M")
                        print(f"Date: {formatted_date}\n")

                        # Show exercise sets for each workout
                        workout_log.view_sets_for_workout(workout_log_id)

                    # Allow the user to save one or all workouts to file
                    while True:
                        print("\nWhat would you like to do?")
                        print("1. Save a specific workout")
                        print("2. Save all workouts")
                        print("3. Go back to the Workout Menu")
                        save_to_file_choice = input(">> ")

                        if save_to_file_choice == '1':
                            # Save a specific workout
                            log_id = input("Enter the Log ID to save: ")
                            if not log_id.isdigit():
                                print("Please enter a valid number")
                                continue

                            log_id = int(log_id)
                            workout_to_save = None
                            for w in workouts:
                                if w[0] == log_id:
                                    workout_to_save = w
                                    break

                            if workout_to_save:
                                workout_log.save_workout_to_file(workout_to_save, log_id)
                                break  # Return to the workout menu after saving
                            else:
                                print("Invalid Log ID")
                        elif save_to_file_choice == '2':
                            # Save all workouts to a single file
                            workout_log.save_all_workouts_to_file(workouts)  # <-- we'll use the new function here
                            break
                        elif save_to_file_choice == '3':
                            # Go back to the workout menu
                            break
                        else:
                            print("Invalid choice. Please enter 1, 2, or 3.")
                    else:
                        print("Workout has not been saved.")

            elif choice_workout_menu == "2":
                # Log a new workout
                workout_log.workout_log(user_id)

            elif choice_workout_menu == "3":
                # View progress - function to be added (Nora's code)
                view_progress()
            elif choice == "4":
                # View favourite workouts - function to be added (Ekta's code)
                view_favorites(cursor, user_id)  # Ekta's code to be added
            elif choice_workout_menu == "5":
                # Go back to main  menu
                continue
            elif choice_workout_menu == "6":
                # Log out
                break
            else:
                print("Invalid choice. Try again.")
        elif choice == "2":
            view_category_workouts()
        elif choice == "3":
            # Log out of the app
            print("Logged out.")
            break
        else:
            print("Invalid choice. Try again.")

#--------------Paula code ------------

"""The ExerciseSearchAPI class provides a simple interface for users to search for workout exercises"
  based on a targeted muscle group using the API Ninjas Exercise API.
  It handles:
  - Taking user input for a muscle group.
  - Sending a GET request to the API with the specified muscle.
  - Displaying the exercise results in a user-friendly format. Paula
  """

class ExerciseSearchAPI:
    def __init__(self, api_key):
        #Initialises the class with API key and API url
        self.api_key = api_key
        self.url = "https://api.api-ninjas.com/v1/exercises"

    def get_muscle_from_user(self):
        # Asks the user to input a muscle, strips leading and trailing spaces and converts it to lower case
        muscle = input("Which type of muscle would you like to work?").strip().lower()

        return muscle

    def get_exercise_api(self, muscle):
        # Gets an exercise using the user's input from the API with the specified muscle group
        exercise_endpoint = f"{self.url}?muscle={muscle}"

        # Sends the GET request to the API with a header containing the API key
        response = requests.get(exercise_endpoint, headers={'X-Api-Key': self.api_key})

        return response

    def display_results_api(self, response):
        # Displays the exercise result
        if response.status_code == 200: #If the request is successful
            exercises = response.json()
            if exercises:#if the result is not empty
                exercise = random.choice(exercises) #picks randomly an exercise from the list
                print(f"Name: {exercise['name']}")
                print(f"Type: {exercise['type']}")
                print(f"Equipment needed: {exercise['equipment']}")
                print(f"Difficulty: {exercise['difficulty']}")
                print(f"Instructions: {exercise['instructions']}")

            else:
                print("No exercises found for this type")#If the list is empty

    def run(self):
        # Main function to run the class
        try:
            muscle = self.get_muscle_from_user()
            response = self.get_exercise_api(muscle)
            self.display_results_api(response)
        except Exception as exc:
            print(f"Something went wrong: {exc}")


"""The ExerciseSearchDB class allows the user to search for exercises from a database.
By selecting a muscle group. It collects input from the user, makes a GET request to an endpoint,
parses the JSON response, and displays the results in a readable format. Paula"""
class ExerciseSearchDB:
    def __init__(self, base_url):
        #Initialises the class with the base URL of the backend AP.
        self.base_url = base_url

    def get_muscle_from_user_db(self):
        # Asks user to input a muscle, removes spaces and converts it to lower case
        return input("Which type of muscle would you like to work?").strip().lower()

    def get_exercises_muscle_db(self, muscle):
        endpoint = f"{self.base_url}/user_exercises" #sets the endpoint url
        params={'muscle': muscle} #add muscle as the query parameter
        response = requests.get(endpoint, params=params) #makes a GET request

        return response.json()

    def display_results_db(self, exercises):
        if exercises: #if the exercises are not empty
            for exercise in exercises:#print the exercises
                print(f"Name: {exercise['name']}")
                print(f"Type: {exercise['type']}")
                print(f"Muscle: {exercise['muscle']}")
                print(f"Difficulty: {exercise['difficulty']}")
                print(f"Equipment needed: {exercise['equipment']}")
                print(f"Instructions: {exercise['instructions']}")
        else:
           print("No exercises found for this muscle.")

    def run(self):
        #Main function to run the class
        try:
            muscle = self.get_muscle_from_user_db() #Asks for user muscle
            exercises = self.get_exercises_muscle_db(muscle)# Gets the exercise from the API
            self.display_results_db(exercises) #Shows the results

        except Exception as exc:
            print(f"Something went wrong: {exc}")


def view_category_workouts():
    use_api= input("Would you like to get an exercise suggestion (a) or get one of your stored exercises(b)? a or b").strip().lower()

    if use_api == 'a':
        exercise_searcher_API = ExerciseSearchAPI(API_KEY)
        exercise_searcher_API.run()
    elif use_api == 'b':
        base_url = "http://127.0.0.1:5000/"
        exercise_searcher_DB = ExerciseSearchDB(base_url)
        exercise_searcher_DB.run()