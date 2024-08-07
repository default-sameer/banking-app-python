from app.session import  load_session
from app.app_initialization import initialize_app
from utils.helpers import display_main_menu
from app.user_management import handle_user_login
from app.customer_management import handle_customer_login
from utils.session_helpers import handle_session_timeout



def main():
    print("Welcome to the Banking Service Application!")
    session = load_session()
    while True:
        if handle_session_timeout(session):
            continue
        display_main_menu(session)
        choice = input("Enter your choice: ")
        if choice == '1':
            handle_user_login(session)
        elif choice == '2':
            handle_customer_login(session)
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
        

if __name__ == "__main__":
    initialize_app()
    main()
