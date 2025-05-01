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

