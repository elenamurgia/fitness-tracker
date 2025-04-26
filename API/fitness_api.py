import os
from socket import create_connection

from flask import Flask, jsonify, request, send_from_directory
from DB.db_utils import ExerciseDB, get_connection

app = Flask(__name__)
exercise_db = ExerciseDB() #creates an instance of ExerciseDB so it can be imported (P)

# Create a connection to the database
conn = get_connection()

# Elena's code (Ref: https://stackoverflow.com/questions/48863061/favicon-ico-results-in-404-error-in-flask-app)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return 'Welcome to the CFG Fitness App'

# Class to fetch a user exercise from the db
@app.route("/user_exercises", methods=["GET"])
def get_exercises_muscle_db():
    muscle = request.args.get("muscle", "").strip().lower()

    #Checks if the muscle parameter is missing or empty
    if not muscle:
        return jsonify({"error": "Missing muscle parameter"}), 400

    #Fetch the exercises from the database for the specified muscle
    exercises = exercise_db.get_exercise_db(muscle)

    return jsonify(exercises)

# Elena's code
# Fetch workouts for a user
@app.route("/<username>/workouts", methods=["GET"])
def get_user_workouts(username):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": f"User '{username}' not found"}), 404
        user_id = result[0]

        cursor.execute("""
            SELECT wl.Workout_log_id, e.name, wl.duration_minutes, wl.notes, wl.log_date
            FROM Workout_Log wl
            JOIN Exercises e ON wl.exercise_id = e.exercise_id
            WHERE wl.user_id = %s
            ORDER BY wl.log_date DESC
        """, (user_id,))
        workouts = cursor.fetchall()

        result = [
            {
                "log_id": row[0],
                "exercise": row[1],
                "duration": row[2],
                "notes": row[3],
                "timestamp": row[4].isoformat()
            }
            for row in workouts
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Log a new workout for a user
@app.route("/<username>/workouts", methods=["POST"])
def log_user_workout(username):   # ✅ match parameter name
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": f"User '{username}' not found"}), 404
        user_id = user[0]

        data = request.get_json()
        exercise_id = data.get("exercise_id")
        duration_minutes = data.get("duration_minutes")
        notes = data.get("notes", "")

        if exercise_id is None or duration_minutes is None:
            return jsonify({"error": "exercise_id and duration_minutes are required"}), 400

        cursor.execute("""
            INSERT INTO Workout_Log (user_id, exercise_id, duration_minutes, notes)
            VALUES (%s, %s, %s, %s)
        """, (user_id, exercise_id, duration_minutes, notes))
        conn.commit()

        return jsonify({"message": "Workout logged successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)