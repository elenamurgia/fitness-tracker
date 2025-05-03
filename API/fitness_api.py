# Initialize DB handler
import requests  # Needed for ExerciseAPI, not request.get
import os
from datetime import datetime, timedelta
# from config import Config # Deborah, do you need this one? I can't see Config in the config.py
from DB.db_utils import WorkoutDiaryDB, ExerciseDB, get_connection
from flask import Flask, jsonify, request, send_from_directory


# --- Flask App Setup ---
app = Flask(__name__)
db = WorkoutDiaryDB()
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

# --- Route: Log Workout to DB ---
@app.route('/api/workout-diary', methods=['POST'])
def log_workout():
    try:
        data = request.get_json()

        user_id = data['user_id']
        exercise_id = data['exercise_id']
        start_time = data.get('start_time', datetime.now().isoformat())
        end_time = data.get('end_time', datetime.now().isoformat())
        duration_minutes = data.get('duration_minutes', 0)
        notes = data.get('notes', '')

        # Insert workout log
        workout_log_id = db.insert_workout_log(
            user_id, exercise_id, start_time, end_time, duration_minutes, notes
        )

        # Insert each set
        for set_data in data.get('sets', []):
            db.insert_exercise_set(
                workout_log_id=workout_log_id,
                set_number=set_data.get('set_number'),
                reps=set_data.get('reps'),
                weight=set_data.get('weight'),
                distance_km=set_data.get('distance_km'),
                duration_seconds=set_data.get('duration_seconds'),
                rest_seconds=set_data.get('rest_seconds')
            )

        return jsonify({"message": "Workout log created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workout-diary', methods=['GET'])
def get_workout_diary():
    user_id = request.args.get('user_id', type=int)
    range_name = request.args.get('range', default="last_7_days")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Define supported date ranges
    today = datetime.today()
    ranges = {
        'last_7_days': (today - timedelta(days=7), today),
        'this_week': (today - timedelta(days=today.weekday()), today),
        'this_month': (today.replace(day=1), today),
        'last_month': (
            (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            today.replace(day=1) - timedelta(days=1)
        ),
        'last_6_months': (today - timedelta(days=180), today)
    }

    # Use default if range not recognized
    start, end = ranges.get(range_name, (today - timedelta(days=7), today))

    try:
        logs = db.get_workout_logs(user_id, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        return jsonify({
            'range': f"{start.date()} to {end.date()}",
            'logs': logs
        })
    except Exception as e:
        print(f"[ERROR] Failed to fetch logs: {e}")
        return jsonify({"error": str(e)}), 500



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
