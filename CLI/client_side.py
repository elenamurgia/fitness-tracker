from AUTH.auth import login, register
from DB.db_utils import get_connection

def main_menu(cursor, conn):
    user_id = None

    while True:
        print("\nFITNESS APP")
        print("Select a number to choose an option:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user_id = login(cursor)
            if user_id:
                logged_in_menu(cursor, conn, user_id)
        elif choice == "2":
            register(cursor, conn)
        elif choice == "3":
            print("Buh-byeeee!")
            break
        else:
            print("Invalid input. Try again.")

def logged_in_menu(cursor, conn, user_id):
    while True:
        # print("\nLogged in")
        print("\nMAIN MENU")
        print("Select a number to choose an option:")
        print("1. View All Workouts")
        print("2. View by Category (arms, legs, chest, etc.)")
        print("3. Log New Workout")
        print("4. View Favorites")
        print("5. Logout")
        choice = input(">> ")

        if choice == "1":
            view_all_workouts(cursor, user_id) # TODO: Will come from class (Al of these are to be modified! just put them here so it's not empty)
        elif choice == "2":
            view_category_workouts(cursor) # TODO: Will come from class
        elif choice == "3":
            log_workout(cursor, conn, user_id) # TODO: Will come from class
        elif choice == "4":
            view_favorites(cursor, user_id) # TODO: Will come from class
        elif choice == "5":
            print("Logged out.")
            break
        else:
            print("Invalid choice. Try again.")
