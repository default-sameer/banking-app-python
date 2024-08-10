from app.customer_management import register_customer
from app.session import update_last_activity
from utils.session_helpers import handle_session_timeout
from utils.validation import validate_date_format

def handle_customer_tasks(session):
    
    while True:
        if handle_session_timeout(session):
            break
        print("\nYeta Bata Customer Add Garne:")
        print("1. Add Customer Account")
        print("2. Edit Customer Details")
        print("3. Delete Customer Account")
        print("4. Back")
        customer_choice = input("Enter your choice: ")
        session = update_last_activity(session)
        if customer_choice == '1':
            name = input("Enter customer's name: ")
            dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
            while not validate_date_format(dob):
                print("Invalid date format. Please enter date in the format YYYY-MM-DD.")
                dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
            account_type = input("Enter account type (savings/current): ").lower()
            account_number, message = register_customer(name, dob, account_type, session['username'])
            if account_number:
                print(f"Customer registered successfully. Account Number: {account_number}, Password: {message}") 
            else:
                print(f"Error: {message}") 
            break
        elif customer_choice == '2':
            print("Edit Customer Details")
        elif customer_choice == '3':
            print("Delete Customer Account")
        elif customer_choice == '4':
            from utils.helpers import back_to_main_menu
            back_to_main_menu(session)
        else:
            print("Invalid choice. Please try again.")