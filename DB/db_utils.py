import mysql.connector
from config import HOST, USER, PASSWORD, DATABASE

def _connect_to_db():
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=DATABASE
    )
    return cnx

if __name__ == "__main__":
    pass