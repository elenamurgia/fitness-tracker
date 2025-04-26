CREATE DATABASE fitness_app;
-- Nora: I made all the tables and column names small caps to keep it consistent and avoid potential typos.

USE fitness_app;

 CREATE TABLE users (
    user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50),
    user_password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
 );

CREATE TABLE exercises (     --data will be taken from the Ninja API and stored in this table
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