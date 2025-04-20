from DB.db_utils import get_connection
from CLI.cliaent_side import main_menu

def run():
    conn = get_connection()
    cursor = conn.cursor()

    print("Welcome to the Fitness App!")
    main_menu(cursor, conn) # Contains login and register functionality

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run()
