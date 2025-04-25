DROP DATABASE IF EXISTS Fitness_app;
CREATE DATABASE Fitness_app;

USE Fitness_app;

 CREATE TABLE Users (
 	user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
     username VARCHAR(50) UNIQUE,
     user_password VARCHAR(255),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
 );

CREATE TABLE Exercises (
    exercise_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    muscle VARCHAR(50),
    difficulty VARCHAR(20),
    equipment VARCHAR(100),
    instructions TEXT
);

CREATE TABLE Workout_Log (
    Workout_log_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INTEGER,
    notes TEXT,

    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (exercise_id) REFERENCES Exercises(exercise_id)
);


CREATE TABLE Exercise_Sets (
    set_id INT NOT NULL,
    Workout_log_id INT NOT NULL,  -- Link to the session-specific exercise entry
    set_number INTEGER NOT NULL,       -- The order of the set (e.g. 1, 2, 3)
    reps INTEGER,
    weight DECIMAL(5,2),
    distance_km DECIMAL(5,2),
    duration_seconds INTEGER,          -- For timed sets
    rest_seconds INTEGER,              -- rest taken before next set

    FOREIGN KEY (Workout_log_id) REFERENCES Workout_Log(Workout_log_id)
);

INSERT INTO Exercises (name, type, muscle, difficulty, equipment, instructions)
VALUES
('Push-Up', 'strength', 'chest', 'beginner', 'none', 'Start in a plank position. Lower your body and push back up.'),
('Squat', 'strength', 'legs', 'beginner', 'none', 'Stand with feet shoulder-width apart. Bend your knees and lower your body.'),
('Bicep Curl', 'strength', 'arms', 'intermediate', 'dumbbells', 'Curl the dumbbells up while keeping your elbows close to your sides.'),
('Plank', 'isometric', 'core', 'intermediate', 'none', 'Hold your body in a straight line, supported on your forearms and toes.'),
('Deadlift', 'strength', 'back', 'advanced', 'barbell', 'Lift the barbell from the floor while keeping your back straight.');