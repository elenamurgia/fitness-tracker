#The WorkoutDiaryDB class handles all interactions with the MySQL database for logging and retrieving workout information.
# It includes methods to insert workout logs (insert_workout_log), save sets of exercises (insert_exercise_set),
# retrieve logs for a user within a date range (get_workout_logs), and fetch individual sets for a specific workout (get_sets_for_workout).
# Each method uses SQL queries to perform actions on the appropriate tables (Workout_Log, Exercise_Sets, Exercises).
# The class manages its own database connection and cursor, and the connection is closed using the close() method when finished. This structure keeps all database-related operations modular and reusable within your fitness app.
import mysql.connector
from config import USER, PASSWORD,HOST,DATABASE

class DbConnectionError(Exception):
    pass

def _connect_to_db():
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        auth_plugin='mysql_native_password',
        password=PASSWORD,
        database=DATABASE
    )
    return connection

def get_all_records(): # retrieve all records from the 'workout logs'
    fitness_api = 'tests'
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        query = """SELECT * FROM Exercises """
        cur.execute(query)
        result = cur.fetchall()  # this is a list with db records where each record is a tuple

        cur.close()

        return result

    except Exception:
        raise DbConnectionError("Failed to read data from DB")



class WorkoutDiaryDB:
    def __init__(self):
        self.conn = _connect_to_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def insert_workout_log(self, user_id, exercise_id, start_time, end_time, duration_minutes, notes):
        query = """
            INSERT INTO Workout_Log (user_id, exercise_id, start_time, end_time, duration_minutes, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, exercise_id, start_time, end_time, duration_minutes, notes))
        self.conn.commit()
        return self.cursor.lastrowid  # Return the new workout_log_id

    def insert_exercise_set(self, workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds):
        query = """
            INSERT INTO Exercise_Sets (
                workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds
        ))
        self.conn.commit()

    def get_workout_logs(self, user_id, start_date, end_date):
        query = """
            SELECT wl.workout_log_id, wl.log_date, wl.duration_minutes, wl.notes,
                   e.name AS exercise_name, e.muscle, e.type
            FROM Workout_Log wl
            JOIN Exercises e ON wl.exercise_id = e.exercise_id
            WHERE wl.user_id = %s AND wl.log_date BETWEEN %s AND %s
            ORDER BY wl.log_date DESC
        """
        self.cursor.execute(query, (user_id, start_date, end_date))
        return self.cursor.fetchall()

    def get_sets_for_workout(self, workout_log_id):
        query = """
            SELECT set_number, reps, weight, distance_km, duration_seconds, rest_seconds
            FROM Exercise_Sets
            WHERE workout_log_id = %s
            ORDER BY set_number
        """
        self.cursor.execute(query, (workout_log_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    print("TESTING DB CONNECTION")
    print (get_all_records())