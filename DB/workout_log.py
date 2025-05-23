# Elena's code
from DB.db_utils import WorkoutDiaryDB

'''
A class to manage logging, viewing and saving workout
sessions and their associated exercise sets
'''
class WorkoutLog:
    # Initialise with a database cursor and connection
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn
        self.db_helper = WorkoutDiaryDB()


    '''
    Allows the user to log a workout by selecting an exercise and entering workout details.
    Additionally logs exercise sets after the main workout entry
    '''
    def workout_log(self, user_id):
        try:
            print("\nAvailable Exercises:")
            # Fetch all the exercises from the database
            self.cursor.execute("SELECT exercise_id, name, muscle, difficulty FROM exercises")
            exercises = self.cursor.fetchall()

            if not exercises:
                print("No exercises found in the database.")
                return

            # Display the exercises with numbering
            for i, exercise in enumerate(exercises, 1):
                print(f"{i}. {exercise[1]} ({exercise[2]}, {exercise[3]})")

            # Ask the user to choose an exercise
            choice = input("\nEnter the number of the exercise you want to log: ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(exercises):
                print("Invalid choice. Please try again.")
                return

            # Get selected exercise details
            selected_exercise = exercises[int(choice) - 1]
            exercise_id = selected_exercise[0]

            # Ask user for duration and optional notes
            duration_minutes = int(input("Duration (in minutes): "))
            notes = input("Any notes or comments that you would like to add? ")

            # Insert workout log into the workout_log table
            workout_log_id = self.db_helper.insert_workout_log(
                user_id, exercise_id, None, None, duration_minutes, notes
            )

        # Ask if the user wants to log the exercise sets
            add_sets = input("Do you want to add sets for this workout? (y/n): ").lower()
            if add_sets == 'y' or add_sets == 'yes':
                print("\nLet's log the exercise sets for this workout.")
                self.add_sets_to_workout(workout_log_id)
            else:
                print("Workout logged without sets")
        except ValueError:
            print("Error logging workout")


    '''
    Allows the user to log multiple sets for a given workout, including reps, 
    weight, distance, duration and rest
    '''
    def add_sets_to_workout(self, workout_log_id):
        set_number = 1
        while True:
            # Collect data for one set
            reps = input(f"Set {set_number} - Repetitions (press Enter to skip): ")
            weight = input(f"Set {set_number} - Weight (Kg) (press Enter to skip): ")
            distance_km = input(f"Set {set_number} - Distance (Km) (press Enter to skip): ")
            duration_seconds = input(f"Set {set_number} - Duration (seconds) (press Enter to skip): ")
            rest_seconds = input(f"Set {set_number} - Rest before next set (seconds) (press Enter to skip): ")

            # Stop loop if no data was entered
            if not reps and not weight and not distance_km and not duration_seconds and not rest_seconds:
                print("No data entered.")
                break

            # Insert the set into the database
            query_exercise_set = '''
            INSERT INTO exercise_sets (workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            self.db_helper.insert_exercise_set(
                workout_log_id,
                set_number,
                int(reps) if reps else None,
                float(weight) if weight else None,
                float(distance_km) if distance_km else None,
                int(duration_seconds) if duration_seconds else None,
                int(rest_seconds) if rest_seconds else None
            )

            # Prompt for next set
            set_number += 1
            more_sets = input("Add another set? (y/n): ").lower()
            if more_sets != 'y' and more_sets != 'yes':
                break
        print("Exercise sets logged successfully!")


    '''
    Retrieves and returns all workouts logged by the user, sorted by date.
    '''
    def view_all_logged_workouts(self, user_id):
        try:
            workout_query = '''
            SELECT wl.workout_log_id, e.name, wl.duration_minutes, wl.notes,wl.log_date
            FROM workout_log wl
            JOIN exercises e ON wl.exercise_id = e.exercise_id
            WHERE wl.user_id = %s
            ORDER BY wl.log_date DESC
            '''
            self.cursor.execute(workout_query, (user_id,))
            workouts = self.cursor.fetchall()

            if not workouts:
                print("You haven't logged any workout yet.")

            return workouts

        except ValueError:
            print("Error retrieving workouts.")

    # Display all exercise sets for a specific workout
    def view_sets_for_workout(self, workout_log_id):

        set_query = '''
        SELECT set_number, reps, weight, distance_km, duration_seconds, rest_seconds
        FROM exercise_sets
        WHERE workout_log_id = %s
        ORDER BY set_number ASC
        '''
        self.cursor.execute(set_query, (workout_log_id,))
        sets = self.cursor.fetchall()

        if sets:
            print("\nExercise Sets:")
            for s in sets:
                print(f"Set {s[0]}:")
                print(f"Reps: {s[1] if s[1] is not None else 'N/A'}")
                print(f"Weight: {s[2] if s[2] is not None else 'N/A'}")
                print(f"Distance: {s[3] if s[3] is not None else 'N/A'}")
                print(f"Duration: {s[4] if s[4] is not None else 'N/A'}")
                print(f"Rest: {s[5] if s[5] is not None else 'N/A'}")
        else:
            print("No sets recorded for this workout.")

    # Save a specific workout and its sets to a text file
    def save_workout_to_file(self, workout, workout_log_id):
        filename = f"workout_log_{workout_log_id}.txt"
        with open(filename, "w") as f:
            f.write(f"Workout Log ID: {workout[0]}\n")
            f.write(f"Exercise: {workout[1]}\n")
            f.write(f"Duration: {workout[2]} minutes\n")
            f.write(f"Notes: {workout[3]}\n")
            formatted_date = workout[4].strftime("%-d %B %Y at %H:%M")
            f.write(f"Date: {formatted_date}\n\n")

            # Get sets from the database
            set_query = '''
            SELECT set_number, reps, weight, distance_km, duration_seconds, rest_seconds
            FROM exercise_sets
            WHERE workout_log_id = %s
            ORDER BY set_number ASC
            '''
            self.cursor.execute(set_query, (workout_log_id,))
            sets = self.cursor.fetchall()

            # Write sets to the file
            if sets:
                f.write("Exercise Sets:\n")
                for s in sets:
                    f.write(f" Set {s[0]}:\n")
                    f.write(f"  Reps: {s[1] if s[1] is not None else 'N/A'}\n")
                    f.write(f"  Weight: {s[2]} Kg\n" if s[2] is not None else "  Weight: N/A\n")
                    f.write(f"  Distance: {s[3]} Km\n" if s[3] is not None else "  Distance: N/A\n")
                    f.write(f"  Duration: {s[4]} seconds\n" if s[4] is not None else "  Duration: N/A\n")
                    f.write(f"  Rest: {s[5]} seconds\n" if s[5] is not None else "  Rest: N/A\n")
            else:
                f.write("No sets recorded for this workout.\n")
        print(f"Workout saved to {filename}!")


    '''
    Saves all workout and their sets to a single text file.
    '''
    def save_all_workouts_to_file(self, workouts):
        filename = "all_workouts.txt"
        with open(filename, "w") as f:
            for workout in workouts:
                workout_log_id = workout[0]
                f.write(f"Workout Log ID: {workout[0]}\n")
                f.write(f"Exercise: {workout[1]}\n")
                f.write(f"Duration: {workout[2]} minutes\n")
                f.write(f"Notes: {workout[3]}\n")
                formatted_date = workout[4].strftime("%-d %B %Y at %H:%M")
                f.write(f"Date: {formatted_date}\n\n")

                # Fetch sets for each workout
                set_query = '''
                SELECT set_number, reps, weight, distance_km, duration_seconds, rest_seconds
                FROM exercise_sets
                WHERE workout_log_id = %s
                ORDER BY set_number ASC
                '''
                self.cursor.execute(set_query, (workout_log_id,))
                sets = self.cursor.fetchall()

                if sets:
                    f.write("Exercise Sets:\n")
                    for s in sets:
                        f.write(f" Set {s[0]}:\n")
                        f.write(f"  Reps: {s[1] if s[1] is not None else 'N/A'}\n")
                        f.write(f"  Weight: {s[2]} Kg\n" if s[2] is not None else "  Weight: N/A\n")
                        f.write(f"  Distance: {s[3]} Km\n" if s[3] is not None else "  Distance: N/A\n")
                        f.write(f"  Duration: {s[4]} seconds\n" if s[4] is not None else "  Duration: N/A\n")
                        f.write(f"  Rest: {s[5]} seconds\n" if s[5] is not None else "  Rest: N/A\n")
                    f.write("\n")
                else:
                    f.write("No sets recorded for this workout.\n\n")
        print(f"All workouts have been saved to {filename}!")
