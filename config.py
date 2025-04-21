# If not already present, create a .env file in the same directory as this script with your database credentials

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

db_config = {
    "DB_HOST": os.getenv("DB_HOST"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_NAME": os.getenv("DB_NAME")
    # Add API key
}

