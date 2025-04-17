# If not already present, create a .env.txt file in the same directory as this script with your database credentials

def load_db_config(path=".env.txt"): # default path to .env.txt
    config = {}
    with open(path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key] = value
    return config

db_config = load_db_config()
