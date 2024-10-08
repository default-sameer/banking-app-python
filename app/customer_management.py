import os
from app.session import save_session, update_last_activity
from utils.constants import CUSTOMERS_FILE, ACCOUNTS_FILE
from utils.generators import generate_unique_customer_id, generate_unique_account_number
from utils.session_helpers import handle_session_timeout
import getpass
from app.service.customer import check_available_balance, update_account_balance, load_customer_data, generate_report

from utils.validation import validate_account_type, validate_date_format
from app.service.customer import update_account_balance, log_transaction, change_customer_password


def ensure_file_exists(file_path, file_description):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                pass
    else:
        print(f"{file_description} not found. Please wait...")
        with open(file_path, 'w') as file:
            print(f"{file_description} created successfully.")

def load_customers():
    ensure_file_exists(CUSTOMERS_FILE, "Customers file")

def load_accounts():
    ensure_file_exists(ACCOUNTS_FILE, "Accounts file") 
            


def register_customer(name, dob, account_type, created_by):
    if not validate_account_type(account_type):
        return None, "Invalid account type. Please choose either 'savings' or 'current'."

    with open(CUSTOMERS_FILE, 'r') as file:
        for line in file:
            customer_id, existing_name, existing_dob, existing_account_type, account_number, password, creator = line.strip().split(',')
            if existing_name == name and existing_dob == dob:
                return None, "Customer with the same name and date of birth already registered."

    customer_id = generate_unique_customer_id()
    account_number = generate_unique_account_number()
    default_password = "password123"
    
    with open(CUSTOMERS_FILE, 'a') as file:
        file.write(f"{customer_id},{name},{dob},{account_type},{account_number},{default_password},{created_by}\n")
    if account_type == 'savings':
        with open(ACCOUNTS_FILE, 'a') as file:
            file.write(f"{customer_id},{name},{account_number},{account_type}, 100 \n")
        update_account_balance(account_number, 100, 'deposit')
        log_transaction(account_number, name, 100, 'deposit')
    else :
        with open(ACCOUNTS_FILE, 'a') as file:
            file.write(f"{customer_id},{name},{account_number},{account_type}, 500 \n")
        update_account_balance(account_number, 500, 'deposit')
        log_transaction(account_number, name, 500, 'deposit')
    return account_number, default_password
    
 
def customer_login():
    account_number = input("Enter your account number: ")
    password_input = getpass.getpass("Enter your password: ")
    
    customer = load_customer_data()
    
    for data in customer:
        if data['account_number'] == account_number and data['password'] == password_input:
            print("Login successful!")
            return data
    print("Invalid account number or password.")
    return None


def handle_customer_login(session):
    if 'customer' in session and 'account_number' in session:
        print(f"Welcome back, {session['customer']}")
        handle_customer_tasks(session)
    else:
        customer = customer_login()
        if customer:
            session['customer'] = customer['name']
            session['account_number'] = customer['account_number']
            session = update_last_activity(session)
            print(f"Welcome, {customer['name']}")
            handle_customer_tasks(session)

def handle_customer_tasks(session):
    while True:
        if handle_session_timeout(session):
            break
        print(f"\nLogged in as: {session['customer']}")
        print("1. View Account Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Change Password")
        print("5. Generate Statement of Account")
        print("6. Logout")
        customer_choice = input("Enter your choice: ")
        session = update_last_activity(session)
        if customer_choice == '1':
            success, message = check_available_balance(session['account_number'])
            if success:
                print(message)
        elif customer_choice == '2':
            amount = input("Enter amount to deposit: ")
            success, message = update_account_balance(session['account_number'], amount, 'deposit')
            if success:
                print(message)
            else: 
                print(message)
        elif customer_choice == '3':
            amount = input("Enter amount to withdraw: ")
            success, message = update_account_balance(session['account_number'], amount, 'withdraw')
            if success:
                print(message)
            else: 
                print(message)
        elif customer_choice == '4':
            password = getpass.getpass("Enter new password: ")
            success, message = change_customer_password(session['customer'] ,session['account_number'], password)
            if(success):
                print(message)
            else:
                print(message)
        elif customer_choice == '5':
            startData = input("Enter start date (YYYY-MM-DD): ")
            endData = input("Enter end date (YYYY-MM-DD): ")
            while not validate_date_format(startData) or not validate_date_format(endData):
                print("Invalid date format. Please enter date in the format YYYY-MM-DD.")
                startData = input("Enter start date (YYYY-MM-DD): ")
                endData = input("Enter end date (YYYY-MM-DD): ")
            success, message = generate_report( session['customer'], session['account_number'], startData, endData)
            if success:
                print(message)
            else:
                print(message)
        elif customer_choice == '6':
            print("Logging out...")
            session.clear()
            save_session(session)
            break