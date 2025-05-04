# 🏋️ Fitness-tracker App
A full-stack fitness tracker app that allows users to:
- Explore exercises (from an external API or the local database).
- Log workouts and sets.
- Track reps, durations, distances and rest periods.
- Save favourite routines

---

## 🧑‍💻 Setup Instructions:

### 1. Clone the repository
```bash
git clone https://github.com/elenamurgia/fitness-tracker.git
cd fitness-tracker
```
### 2. Create an `.env` file 
Create a `.env` file in the root directory and include your database and API credentials: 

```env
DB_HOST = "your Local Host"
DB_USER = "your username"
DB_PASSWORD = "your Password”
DB_NAME = "fitness_app"
API_KEY = 'your_api_key'
```


## Running the App
### 1. Run the backend Flask API 
```bash
python fitness_api.py
```
### 2. Run the terminal app
```bash
python app.py
```
For Windows/PyCharm users: use the terminal and write python app.py to run the script and see the instructions in the terminal.

## 📋 How to Use the App

### 🔐 Authentication 
* To **register** (option number 2), prompt your username and password, and press Enter.
![A screenshot](https://raw.githubusercontent.com/elenamurgia/fitness-tracker/main/Images/Screenshot_reg_terminal.png "Screenshot register terminal")

* To **log in**, choose option 1 and enter your username and password. If the data is not correct, a message will be displayed.
![A screenshot](https://raw.githubusercontent.com/elenamurgia/fitness-tracker/main/Images/Screenshot_login_terminal.png "Screenshot login terminal")
If the login is successful, a message will be displayed to confirm that the user is logged in, and the Main Menu will appear.

1. If the user chooses 1, they could choose between view past workouts or log new workouts:
![A screenshot](https://raw.githubusercontent.com/elenamurgia/fitness-tracker/main/Images/Screenshot_workout_terminal.png "Screenshot workout terminal")

2. If the user chooses 2, they could choose between getting a new exercise suggestion or one of the stored exercises:
Option a (new suggestion from the Ninjas API exercises).
![A screenshot](https://raw.githubusercontent.com/elenamurgia/fitness-tracker/main/Images/Screenshot_api_exercise.png "Screenshot api exercise")

Option b (exercises related to the muscle from the stored exercises).
![A screenshot](https://raw.githubusercontent.com/elenamurgia/fitness-tracker/main/Images/Screenshot_exercise_suggestion_menu.png "Screenshot exercise suggestion terminal")

## 🧪 Technologies & Imports

**Python Libraries Used:**

```python
import os
import getpass
import random
import requests
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
```

**Third-party packages (install via pip):**

```bash
pip install flask python-dotenv mysql-connector-python requests
```

---

## Features Implemented

- [x] User authentication (register/login)
- [x] Log and view workouts
- [x] Add and retrieve sets for each workout
- [x] Get exercise suggestions from API or DB
- [x] Save workouts to file


---

## Features in Progress

- [ ] View progress charts
- [ ] Favourite exercises
- [ ] Multi-user leaderboard or competition mode

---

## Contributors

- Elena Murgia  
- Paula Calvo  
- Deborah Kamanya  
- Nora Rodriguez  
- Amber Mahmood  
- Ekta Shah  
