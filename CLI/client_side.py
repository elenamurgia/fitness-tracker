
#Deborah's Code
import requests
import json
from datetime import datetime
from DB.db_utils import WorkoutDiaryDB
db = WorkoutDiaryDB()
# Base URL for your local Flask API
BASE_URL = "http://127.0.0.1:5000/api"

def view_logs():
    print("=== View Workout Logs ===")

    # Prompt user to choose a user_id and time range
    user_id = int(input("User ID: "))
    range_name = input("Range (e.g., last_7_days, this_month,last_month, last_6_months): ")

    params = {
        "user_id": user_id,
        "range": range_name
    }

    # Send GET request to fetch logs
    try:
        response = requests.get(f"{BASE_URL}/workout-diary", params=params)
        response.raise_for_status()
        data = response.json()

        print("Retrieved workout logs:")
        for log in data.get("logs", []):
            print(f"\n Date: {log['log_date']} |  Exercise: {log['exercise_name']} ({log['muscle']})")
            print(f"Duration: {log['duration_minutes']} mins | Notes: {log['notes']}")
            print("Sets:")
            for s in log.get("sets", []):
                print(f"  - Set {s['set_number']}: {s['reps']} reps x {s['weight']}kg (Rest: {s['rest_seconds']}s)")

    except requests.RequestException as e:
        print(" Error fetching logs:", e)


# class WorkoutClient:
#     def __init__(self):
#         # Headers to indicate we're sending/receiving JSON
#         self.headers = {"Content-Type": "application/json"}
#
#     def log_workout(self):
#         print("=== Log a New Workout ===")
#
#         # Prompt user for workout details
#         user_id = int(input("User ID: "))
#         exercise_id = int(input("Exercise ID: "))
#
#         # Datetime inputs default to "now" in ISO format
#         print("Use format YYYY-MM-DDT HH:MM:SS or press Enter for current time")
#         start_time = input("Start time [Enter for now]: ") or datetime.now().isoformat()
#         end_time = input("End time [Enter for now]: ") or datetime.now().isoformat()
#         duration = int(input("Duration in minutes: "))
#         notes = input("Any notes? (optional): ")
#
#         # Prompt for multiple sets
#         num_sets = int(input("How many sets?: "))
#         sets = []
#         for i in range(num_sets):
#             print(f"--- Set {i + 1} ---")
#             set_number = i + 1
#             reps = int(input("Reps: "))
#             weight = float(input("Weight (kg): "))
#             distance = input("Distance (km) [optional]: ") or None
#             duration_seconds = input("Duration (seconds) [optional]: ") or None
#             rest = input("Rest (seconds): ")
#
#             sets.append({
#                 "set_number": set_number,
#                 "reps": reps,
#                 "weight": weight,
#                 "distance_km": float(distance) if distance else None,
#                 "duration_seconds": int(duration_seconds) if duration_seconds else None,
#                 "rest_seconds": int(rest)
#             })
#
#         # Construct the JSON payload
#         payload = {
#             "user_id": user_id,
#             "exercise_id": exercise_id,
#             "start_time": start_time,
#             "end_time": end_time,
#             "duration_minutes": duration,
#             "notes": notes,
#             "sets": sets
#         }
#
#         # Send POST request to log workout
#         response = requests.post(f"{BASE_URL}/workout-diary", headers=self.headers, data=json.dumps(payload))
#
#         # Handle the response
#         if response.status_code == 201:
#             print("Workout successfully logged!")
#         else:
#             try:
#                 print(" Failed to log workout:", response.json())
#             except ValueError:
#                 print(" Failed to log workout. Response:", response.text)
#
#
# def run():
#     client = WorkoutClient()
#     while True:
#         print("\n--- Workout CLI ---")
#         print("[1] Log Workout")
#         print("[2] View Logs")
#         print("[0] Exit")
#         choice = input("Choose an option: ")
#         if choice == "1":
#             client.log_workout()
#         elif choice == "2":
#             view_logs()
#         elif choice == "0":
#             break
#         else:
#             print(" Invalid option.")
#
# if __name__ == "__main__":
#     run()

