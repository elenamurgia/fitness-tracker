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
            db_connection = self.connector.get_connection()
            cur = db_connection.cursor()
            print("Connected to DB")#Debug message

            query = """
                SELECT exercise_id, name, type, muscle, difficulty, equipment, instructions
                FROM Exercises
                WHERE muscle = %s"""

            cur.execute(query, (muscle,))

            #Fetches all the results from the query
            rows = cur.fetchall()
            #Define the column names to map the result rows to dictionary keys
            columns = ['exercise_id', 'name', 'type', 'muscle', 'difficulty', 'equipment', 'instructions']
            #Create a list of dictionaries by pairing column names with the values from each row
            result = [dict(zip(columns,row)) for row in rows]

            cur.close()

            return result


        finally:
            if db_connection:
                db_connection.close()
                print("DB connection is closed")#Debug message
