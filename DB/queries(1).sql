DROP DATABASE IF EXISTS fitness_app;
CREATE DATABASE fitness_app;
-- Nora: I made all the tables and column names small caps to keep it consistent and avoid potential typos.

USE fitness_app;

 CREATE TABLE users (
    user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50),
    user_password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
 );

CREATE TABLE exercises (     -- data will be taken from the Ninja API and stored in this table
    exercise_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    muscle VARCHAR(50),
    difficulty VARCHAR(20),
    equipment VARCHAR(100),
    instructions TEXT
);

CREATE TABLE workout_log (
    workout_log_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INTEGER,
    notes TEXT,

    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);


CREATE TABLE exercise_sets (
    set_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    workout_log_id INTEGER NOT NULL,  -- Link to the session-specific exercise entry
    set_number INTEGER NOT NULL,       -- The order of the set (e.g. 1, 2, 3)
    reps INTEGER,
    weight DECIMAL(5,2),
    distance_km DECIMAL(5,2),
    duration_seconds INTEGER,          -- For timed sets
    rest_seconds INTEGER,              -- rest taken before next set

    FOREIGN KEY (workout_log_id) REFERENCES workout_log(workout_log_id)
);


-- Mock data for Elena's tests
INSERT INTO users (username, user_password)
VALUES
('tester', 'test123');


-- Mock data for Elena's tests
INSERT INTO Exercises (name, type, muscle, difficulty, equipment, instructions)
VALUES
('Push-Up', 'strength', 'chest', 'beginner', 'none', 'Start in a plank position. Lower your body and push back up.'),
('Squat', 'strength', 'legs', 'beginner', 'none', 'Stand with feet shoulder-width apart. Bend your knees and lower your body.'),
('Bicep Curl', 'strength', 'arms', 'intermediate', 'dumbbells', 'Curl the dumbbells up while keeping your elbows close to your sides.'),
('Plank', 'isometric', 'core', 'intermediate', 'none', 'Hold your body in a straight line, supported on your forearms and toes.'),
('Deadlift', 'strength', 'back', 'advanced', 'barbell', 'Lift the barbell from the floor while keeping your back straight.'),
('Lunges', 'strength', 'legs', 'beginner', 'none', 'Step forward with one leg and lower your hips until both knees are bent at about 90 degrees.'),
('Tricep Dip', 'strength', 'arms', 'beginner', 'bench', 'Use a bench or chair to dip your body down and push back up using your triceps.'),
('Mountain Climbers', 'cardio', 'core', 'intermediate', 'none', 'In a plank position, alternate bringing your knees to your chest as fast as you can.'),
('Russian Twist', 'strength', 'core', 'intermediate', 'medicine ball', 'Sit with knees bent, lean back slightly, and twist your torso side to side.'),
('Burpees', 'cardio', 'full body', 'advanced', 'none', 'Squat, jump to a plank, do a push-up, jump forward and leap up.'),
('Bench Press', 'strength', 'chest', 'intermediate', 'barbell', 'Lie on a bench and press the barbell up from your chest.'),
('Leg Press', 'strength', 'legs', 'intermediate', 'machine', 'Push the weight platform away with your legs while seated in the machine.'),
('Lat Pulldown', 'strength', 'back', 'intermediate', 'machine', 'Pull the bar down to your chest, keeping your back straight and elbows down.'),
('Side Plank', 'isometric', 'core', 'intermediate', 'none', 'Lie on one side and lift your body using one forearm, keeping your body straight.'),
('Jump Rope', 'cardio', 'full body', 'beginner', 'jump rope', 'Jump continuously while rotating the rope with your wrists.');

-- Mock data for Elena's tests
INSERT INTO workout_log (user_id, exercise_id, duration_minutes, notes)
VALUES
(1, 1, 30, 'Test workout');

-- Mock data for Elena's tests
INSERT INTO exercise_sets (workout_log_id, set_number, reps, weight, distance_km, duration_seconds, rest_seconds)
VALUES
(1, 1, 10, 40.0, NULL, 60, 30),
(1, 2, 8, 45.0, NULL, 55, 30);