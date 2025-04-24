# Initialize DB handler
from datetime import datetime, timedelta
from config import Config
from DB.db_utils import WorkoutDiaryDB
from flask import Flask, request, jsonify
import requests  # Needed for ExerciseAPI, not request.get

# --- Flask App Setup ---
app = Flask(__name__)
db = WorkoutDiaryDB()



EXERCISE_API_URL = "https://api.api-ninjas.com/v1/exercises"
API_KEY = Config.API_NINJAS_KEY  # Store this in config.py securely
# used to test api data
@app.route('/api/exercise-search', methods=['GET'])
def search_exercise():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide an exercise name using the 'name' query param"}), 400

    try:
        response = requests.get(EXERCISE_API_URL, params={"name": name}, headers={"X-Api-Key": API_KEY})
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

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


# --- App Entry Point ---
if __name__ == "__main__":
    app.run(debug=True)