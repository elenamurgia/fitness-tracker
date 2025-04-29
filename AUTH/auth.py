import getpass
import mysql.connector

class UserAuth:
    def __init__(self, db_cursor, db_conn):
        self.cursor = db_cursor
        self.conn = db_conn

    def login(self):
        """Handles user login."""
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        print(f"DEBUG: Looking for username: {username} and password: {password}")  # Debugging line

        query = "SELECT user_id FROM Users WHERE username = %s AND user_password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            print(f"Login successful. Welcome, {username}!")
            return result[0]
        else:
            print("Invalid username or password.")
            return None

    def register(self):
        """Handles user registration."""
        print("Debug: Entered register()") #Debug line
        username = input("Choose a username: ").strip()
        password = getpass.getpass("Choose a password: ").strip()
        print(f"DEBUG: Looking for username: {username} and password: {password}")  # Debugging line

        try:
            self.cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            if self.cursor.fetchone():
                print("Username already exists. Try another.")
                return

            print("DEBUG: Inserting new user now...")
            self.cursor.execute(
                "INSERT INTO Users (username, user_password) VALUES (%s, %s)",
                (username, password)
            )
            self.conn.commit()
            print("Registration successful. You can now log in.")
            input("Press Enter to return to the main menu.")
        except Exception as e:
            print(f"Registration failed: {e}")
            return None