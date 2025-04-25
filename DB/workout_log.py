class WorkoutLog:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def workout_log(self, user_id):
        try:
            print("\nAvailable Exercises:")
            self.cursor.execute("SELECT exercise_id, name, muscle, difficulty FROM Exercises")
            exercises = self.cursor.fetchall()

            if not exercises:
                print("No exercises found in the database.")
                return

            for i, exercise in enumerate(exercises, 1):
                print(f"{i}. {exercise[1]} ({exercise[2]}, {exercise[3]})")

            choice = input("\nEnter the number of the exercise you want to log: ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(exercises):
                print("Invalid selection. Try again.")
                return

            selected_exercise = exercises[int(choice) - 1]
            exercise_id = selected_exercise[0]
            duration = int(input("Duration (in minutes): "))
            notes = input("Any notes or comments that you would like to add? ")

            query = '''
            INSERT INTO Workout_Log (user_id, exercise_id, duration_minutes, notes)
            VALUES (%s, %s, %s, %s)
            '''
            self.cursor.execute(query, (user_id, exercise_id, duration, notes))
            self.conn.commit()
            print("Workout logged successfully!")

        except Exception as e:
            print(f"Error logging workout: {e}")

    def view_all_workouts(self, user_id):
        try:
            query = '''
            SELECT wl.Workout_log_id, e.name, wl.duration_minutes, wl.notes,wl.log_date
            FROM Workout_log wl
            JOIN Exercises e ON wl.exercise_id = e.exercise_id
            WHERE wl.user_id = %s
            ORDER BY wl.log_date DESC
            '''
            self.cursor.execute(query, (user_id,))
            workouts = self.cursor.fetchall()

            if not workouts:
                print("You haven't logged any workout yet.")
                return

            print("\n Your workout Log: ")
            for w in workouts:
                print(f"Log ID: {w[0]}")
                print(f"Exercise: {w[1]}")
                print(f"Duration: {w[2]} minutes")
                print(f"Notes: {w[3]}")
                print(f"Date: {w[4]}\n")
        except Exception as e:
            print(f"Error retrieving workouts: {e}")


