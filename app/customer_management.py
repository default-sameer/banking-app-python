import os
from app.session import save_session, update_last_activity
from utils.constants import CUSTOMERS_FILE, ACCOUNTS_FILE
from utils.generators import generate_unique_customer_id, generate_unique_account_number
from utils.session_helpers import handle_session_timeout
import getpass

# Function to load existing customer data from file
def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as file:
            for line in file:
                # Process each line (e.g., create Customer objects)
                pass
    else:
        print("Customers file not found. Please wait...")
        with open(CUSTOMERS_FILE, 'w') as file:
            print("Customers file created successfully.")
            
        

# Function to load existing account data from file
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as file:
            for line in file:
                # Process each line (e.g., create Account objects)
                pass
    else:
        # Handle case where file doesn't exist
        print("Accounts file not found. Please wait...")
        with open(ACCOUNTS_FILE, 'w') as file:
            print("Accounts file created successfully.")   
            
            
def load_customer_data():
    customers = []
    with open(CUSTOMERS_FILE, 'r') as file:
        for line in file:
            customer_id, name, dob, account_type, account_number, password = line.strip().split(',')
            customers.append({'customer_id': customer_id, 'name': name, 'dob': dob, 'account_type': account_type, 'account_number': account_number, 'password': password})
    return customers


def register_customer(name, dob, account_type):
    with open(CUSTOMERS_FILE, 'r') as file:
        for line in file:
            if name in line:
                return None, "Customer already registered."
    customer_id = generate_unique_customer_id()
    account_number = generate_unique_account_number()
    default_password = "password123"
    with open(CUSTOMERS_FILE, 'a') as file:
        file.write(f"{customer_id},{name},{dob},{account_type},{account_number},{default_password}\n")
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
    customer = customer_login()
    if customer:
        session['customer'] = customer['name']
        session = update_last_activity(session)
        print(f"Welcome, {customer['name']}")
        handle_customer_tasks(session)

def handle_customer_tasks(session):
    while True:
        if handle_session_timeout(session):
            break
        print("\nCustomer Menu:")
        print("1. View Account Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Change Password")
        print("6. Logout")
        customer_choice = input("Enter your choice: ")
        session = update_last_activity(session)
        if customer_choice == '1':
            print("View Account Balance")
        elif customer_choice == '2':
            print("Deposit Money")
        elif customer_choice == '3':
            print("Withdraw Money")
        elif customer_choice == '4':
            print("Transfer Money")
        elif customer_choice == '5':
            print("Change Password")
        elif customer_choice == '6':
            print("Logging out...")
            session.clear()
            save_session(session)
            break