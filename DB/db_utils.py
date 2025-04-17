from config import db_config
import mysql.connector

# This function creates a connection using the config file (please refer to config file for more instructions)
def get_connection():
    return mysql.connector.connect(
        host=db_config["DB_HOST"],
        user=db_config["DB_USER"],
        password=db_config["DB_PASSWORD"],
        database=db_config["DB_NAME"]
    )
