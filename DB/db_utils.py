
class DbConnectionError(Exception):
    pass
import mysql.connector
DATABASE = "Fitness_app"

def _connect_to_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_user',
        password='your_password',
        database= DATABASE
    )
    return connection


def insert_exercise( name, type_, muscle, difficulty, equipment, instructions):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print('Connected to DB:%s' % DATABASE)

        insert_query = """
                        INSERT INTO exercises (name, type, muscle, difficulty, equipment, instructions)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
        cur.execute(insert_query, (name, type_, muscle, difficulty, equipment, instructions))
        db_connection.commit()

        cur.close()
        return

    except Exception:
        raise DbConnectionError("Failed to add data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def log_exercise_set(user_id, log_date, exercise_id, sets, reps, weight):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cursor = db_connection.cursor()
        print('Connected to DB: %s' % DATABASE)

        insert_query = """
            INSERT INTO workout_log (user_id, workout_date, exercise_id, sets, reps, weight)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, log_date, exercise_id, sets, reps, weight))
        db_connection.commit()

        cursor.close()
        return {
            "success": True,
            "message": "Workout logged successfully.",
            "workout_id": cursor.lastrowid
        }

    except Exception as e:
        print(f"Error logging workout: {e}")
        return {
            "success": False,
            "message": "Failed to log workout.",
            "error": str(e)
        }

    finally:
        if db_connection and db_connection.is_connected():
            db_connection.close()
            print("DB connection is closed.")




def get_workout(user_id, exercise_id, log_date, start_time, end_time, duration_minutes, notes):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        get_workout_query = """
            INSERT INTO workout_log (user_id, exercise_id, log_date, start_time, end_time, duration_minutes, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(get_workout_query, (user_id, exercise_id, log_date, start_time, end_time, duration_minutes, notes))
        db_connection.commit()
        print("Workout logged successfully.")


    except Exception:
        raise DbConnectionError("Failed to add data to DB")


    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def fetch_workouts_with_params(user_id, date_filter_sql, date_values):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        print('Connected to DB: %s' % DATABASE)

        cursor = db_connection.cursor(dictionary=True)
        query = f"""
            SELECT * FROM workout_log
            WHERE user_id = %s AND log_date {date_filter_sql}
            ORDER BY log_date DESC
        """
        cursor.execute(query, (user_id, *date_values))
        results = cursor.fetchall()
        cursor.close()
        return results

    except mysql.connector.Error as err:
        print(f"Error fetching workouts: {err}")
        return []

    finally:
        if db_connection and db_connection.is_connected():
            db_connection.close()


from datetime import datetime, timedelta

def custom_range(user_id, start_date, end_date):
    """
    Fetch workouts for a user between any two dates (inclusive).
    Dates must be in 'YYYY-MM-DD' format.
    """
    date_filter = "BETWEEN %s AND %s"
    return fetch_workouts_with_params(user_id, date_filter, (start_date, end_date))

#def last_7_days(user_id):
#    return fetch_workouts_with_params(user_id, ">= CURDATE() - INTERVAL 7 DAY") # gets all workout from the start of the week to today


#def this_week(user_id):
#    return fetch_workouts_with_params(user_id, ">= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)")

#def previous_week(user_id):
#    return fetch_workouts_with_params(user_id, "BETWEEN DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 7 DAY) AND DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 1 DAY)")

#def this_month(user_id):
#    return fetch_workouts_with_params(user_id, ">= DATE_FORMAT(CURDATE(), '%Y-%m-01')")

#def last_month(user_id):
#    return fetch_workouts_with_params(user_id, "BETWEEN DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01') AND LAST_DAY(CURDATE() - INTERVAL 1 MONTH)")

#def last_6_months(user_id):
#    return fetch_workouts_with_params(user_id, ">= CURDATE() - INTERVAL 6 MONTH")

