from app.customer_management import register_customer
from app.session import save_session, update_last_activity
from utils.session_helpers import handle_session_timeout
from utils.validation import validate_date_format
from app.service.customer import delete_customer_account, edit_customer_account_type, generate_report
from utils.validation import validate_account_type, get_account_number_and_dob

def handle_customer_tasks(session):
    while True:
        if handle_session_timeout(session):
            break
        print("\nYeta Bata Customer Add Garne:")
        print("1. Add Customer Account")
        print("2. Edit Account Type")
        print("3. Delete Customer Account")
        print("4. Generate Statement of Account of a Customer")
        print("4. Logout")
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
            account_number, dob = get_account_number_and_dob()
            new_account_type = input("Enter new account type (savings/current): ").lower()
            if not validate_account_type(new_account_type):
                return None, "Invalid account type. Please choose either 'savings' or 'current'."
            success, message = edit_customer_account_type(account_number, dob, new_account_type)
            print(message)
        elif customer_choice == '3':
            account_number, dob = get_account_number_and_dob()
            success, message = delete_customer_account(account_number, dob)
            print(message)
            if success:
                break
        elif customer_choice == '4':
            customer_name = input("Enter customer name: ")
            account_number = input("Enter account number: ")
            startData = input("Enter start date (YYYY-MM-DD): ")
            endData = input("Enter end date (YYYY-MM-DD): ")
            while not validate_date_format(startData) or not validate_date_format(endData):
                print("Invalid date format. Please enter date in the format YYYY-MM-DD.")
                startData = input("Enter start date (YYYY-MM-DD): ")
                endData = input("Enter end date (YYYY-MM-DD): ")
            success, message = generate_report(customer_name, account_number, startData, endData)
            if success:
                print(message)
                break
            else:
                print(message)
        elif customer_choice == '5':
            print("Logging out...")
            session.clear()
            save_session(session)
            break
            
        else:
            print("Invalid choice. Please try again.")