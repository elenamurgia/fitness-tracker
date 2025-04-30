import os
from flask import Flask, jsonify, request, send_from_directory
from DB.db_utils import ExerciseDB, get_connection

app = Flask(__name__)
exercise_db = ExerciseDB() #creates an instance of ExerciseDB so it can be imported (P)

# Create a connection to the database
conn = get_connection()
app.config['db_connection'] = conn

# Elena's code (Ref: https://stackoverflow.com/questions/48863061/favicon-ico-results-in-404-error-in-flask-app)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return 'Welcome to the CFG Fitness App'

# Fetch a user exercise from the db
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
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if not result:
        return jsonify(f"User '{username}' not found"), 404
    user_id = result[0]

    cursor.execute("""
        SELECT wl.workout_log_id, e.name, wl.duration_minutes, wl.notes, wl.log_date
        FROM workout_Log wl
        JOIN exercises e ON wl.exercise_id = e.exercise_id            WHERE wl.user_id = %s
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

# Log a new workout for a user
@app.route("/<username>/workouts", methods=["POST"])
def log_user_workout(username):
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify(f"User '{username}' not found"), 404
    user_id = user[0]

    data = request.get_json()
    exercise_id = data.get("exercise_id")
    duration_minutes = data.get("duration_minutes")
    notes = data.get("notes", "")

    if exercise_id is None or duration_minutes is None:
        return jsonify({"error": "exercise_id and duration_minutes are required"}), 400

    cursor.execute("""
                    INSERT INTO workout_log (user_id, exercise_id, duration_minutes, notes)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, exercise_id, duration_minutes, notes))
    conn.commit()

    return jsonify({"message": "Workout logged successfully!"}), 201


# Fetch sets for a specific workout
@app.route("/<username>/<int:workout_log_id>/sets", methods=["GET"])
def get_workout_sets(username, workout_log_id):
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": f"User '{username}' not found"}), 404

    cursor.execute("""
        SELECT set_number, reps, weight, distance_km, duration_seconds, rest_seconds
        FROM exercise_sets
        WHERE workout_log_id = %s
        ORDER BY set_number ASC
    """, (workout_log_id,))
    sets = cursor.fetchall()

    if not sets:
        return jsonify({"message": "No sets found for this workout"}), 404

    result = [
        {
            "set_number": row[0],
            "reps": row[1],
            "weight": row[2],
            "distance_km": row[3],
            "duration_seconds": row[4],
            "rest_seconds": row[5]
        }
        for row in sets
    ]

    return jsonify(result), 200


# Log a set for a specific workout
@app.route("/<username>/<int:workout_log_id>/sets", methods=["POST"])
def add_set_to_workout(username, workout_log_id):
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify(f"User '{username}' not found"), 404

    data = request.get_json()

    set_number = data.get("set_number")
    if set_number is None:
        return jsonify({"error": "Missing required field: set_number"}), 400

    reps = data.get("reps")
    weight = data.get("weight")
    distance_km = data.get("distance_km")
    duration_seconds = data.get("duration_seconds")
    rest_seconds = data.get("rest_seconds")

    insert_query = '''
    INSERT INTO exercise_sets (workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds))
    conn.commit()

    return jsonify({"message": "Set logged successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
