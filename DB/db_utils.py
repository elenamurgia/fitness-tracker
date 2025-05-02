from config import db_config
import mysql.connector

#This function creates a connection using the config file (please refer to config file for more instructions)
def get_connection():
    return mysql.connector.connect(
        host=db_config["DB_HOST"],
        user=db_config["DB_USER"],
        password=db_config["DB_PASSWORD"],
        database=db_config["DB_NAME"]
    )

#--------------Paula code-----------
"""The ExerciseDB class interacts with the database to fetch exercise data based 
on the user's specified muscle group."""
class ExerciseDB:
    def __init__(self):
        self.connector = get_connection()

    def get_exercise_db(self, muscle):
        db_connection = None
        try:
            db_connection = get_connection()
            cur = db_connection.cursor()
            print("Connected to DB")#Debug message

            query = """
                SELECT exercise_id, name, type, muscle, difficulty, equipment, instructions
                FROM Exercises
                WHERE muscle = %s"""

            cur.execute(query, (muscle,))

            #Fetches all the results from the query
            rows = cur.fetchall()

            result = [
                {"exercise_id": row[0],
                 "name": row[1],
                 "type": row[2],
                 "muscle": row[3],
                 "difficulty": row[4],
                 "equipment": row[5],
                 "instructions": row[6],
                 }
                for row in rows
            ]
            return result

        finally:
            if db_connection:
                db_connection.close()


#--------------Nora's code-----------
"""
The UserProgressTracker class interacts with the database to fetch workout data and
calculate and compare it between 2 periods of time.

Tracks the progress by comparing the last 7 days of workouts vs the previous
7-day period. It helps see improvements in amount of workouts done and
total time worked out.
"""
class UserProgressTracker:
    def __init__(self):
        self.connector = get_connection()

    # Handles user progress claculations on demand.
    def get_7day_progress(self, user_id):
        db_connection = None

        try:
            db_connection = get_connection()
            cur = db_connection.cursor()
            print("Connected to DB")#Debug message

            # SQL Query to fetch data from the workout_log table
            query = """ 
                SELECT 
                    (SELECT COUNT(*) FROM workout_log 
                    WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS recent_workouts,
                    
                    (SELECT COALESCE(SUM(duration_minutes), 0) FROM workout_log
                    WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS recent_minutes,
                                    
                    (SELECT COUNT(*) FROM workout_log 
                    WHERE user_id = %s AND log_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 14 DAY)
                    AND DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS previous_workouts,

                    (SELECT COALESCE(SUM(duration_minutes), 0) FROM workout_log
                    WHERE user_id = %s AND log_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 14 DAY)
                    AND DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS previous_minutes 
                
                """
            
            # user_id 4 times because SQL query has 4 subqueries, each needing a parameter user_id.
            cur.execute(query, (user_id, user_id, user_id, user_id))
            recent_w, recent_m, previous_w, previous_m = cur.fetchone()

            # Put the result of the query into a dictionary with 4 variabes
            result = {
                'current_workouts': recent_w,
                'current_minutes': recent_m,
                'workout_difference': recent_w - previous_w,
                'minutes_difference': recent_m - previous_m
            }
            cur.close()

            return result
        
        finally:
            if db_connection:
                db_connection.close()
                print("DB connection is closed")#Debug message