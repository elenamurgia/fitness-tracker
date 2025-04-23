# Initialize DB handler
from flask import Flask, jsonify, request
from datetime import datetime
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

        # Required workout log info
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

if __name__ == "__main__":
    app.run(debug=True)
