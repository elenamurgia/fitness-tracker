CREATE DATABASE Fitness_app; 

USE Fitness_app;

CREATE TABLE Exercises (     --data will be taken from the Ninja API and stored in this table
    exercise_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),            
    muscle VARCHAR(50),           
    difficulty VARCHAR(20),       
    equipment VARCHAR(100),       
    instructions TEXT,            
);

CREATE TABLE Workout_Log (
    Workout_log_id SERIAL PRIMARY KEY,
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


CREATE TABLE Exercise_Sets (
    set_id SERIAL PRIMARY KEY,
    Workout_log_id INTEGER NOT NULL,  -- Link to the session-specific exercise entry
    set_number INTEGER NOT NULL,       -- The order of the set (e.g. 1, 2, 3)
    reps INTEGER,
    weight DECIMAL(5,2),    
    distance_km DECIMAL(5,2),
    duration_seconds INTEGER,          -- For timed sets
    rest_seconds INTEGER,              -- rest taken before next set

    FOREIGN KEY (Workout_log_id) REFERENCES Workout_Log(Workout_log_id)
);
