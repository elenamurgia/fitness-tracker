from flask import Flask, jsonify, request
from DB.db_utils import ExerciseDB

app = Flask(__name__)
exercise_db = ExerciseDB() #creates an instance of ExerciseDB so it can be imported (P)

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

if __name__ == "__main__":
    app.run(debug=True)