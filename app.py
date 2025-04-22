from DB.db_utils import get_connection
from CLI.client_side import main_menu

def run():
    conn = get_connection()
    cursor = conn.cursor()

    print("Welcome to the Fitness App!")
    main_menu(cursor, conn) # Contains login and register functionality

    cursor.close()
    conn.close()

if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()
    main_menu(cursor, conn)

