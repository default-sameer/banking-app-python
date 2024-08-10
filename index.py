# main.py

import os
from datetime import datetime
from utils.validation import validate_date_format

# Paths to data files
CUSTOMERS_FILE = os.path.join("data", "customers.txt")
ACCOUNTS_FILE = os.path.join("data", "accounts.txt")
TRANSACTIONS_DIR = os.path.join("data", "transactions")

# Function to initialize application and load data
def initialize():
    # Create 'data' directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Create 'transactions' directory if it doesn't exist
    if not os.path.exists(TRANSACTIONS_DIR):
        os.makedirs(TRANSACTIONS_DIR)

    # Example: Load existing customer and account data into memory
    load_customers()
    load_accounts()

# Example function to load existing customer data from file
def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as file:
            for line in file:
                # Process each line (e.g., create Customer objects)
                pass
    else:
        # Handle case where file doesn't exist
        print("Customers file not found.")

# Example function to load existing account data from file
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as file:
            for line in file:
                # Process each line (e.g., create Account objects)
                pass
    else:
        # Handle case where file doesn't exist
        print("Accounts file not found.")

# Example function to register a new customer and save to file
def register_customer(name, address, account_type):
    # Generate customer ID based on current timestamp (for simplicity)
    customer_id = datetime.now().strftime("%Y%m%d%H%M%S")

    # Example: Save customer details to file
    with open(CUSTOMERS_FILE, 'a') as file:
        file.write(f"{customer_id},{name},{address},{account_type}\n")

    # Example: Create account and save to file
    account_number = generate_account_number()
    initial_balance = 0.0  # Default initial balance for new accounts
    with open(ACCOUNTS_FILE, 'a') as file:
        file.write(f"{customer_id},{account_number},{initial_balance}\n")

    return customer_id

# Example function to generate a unique account number
def generate_account_number():
    # Example: Generate account number based on current timestamp (for simplicity)
    return datetime.now().strftime("%Y%m%d%H%M%S")

# Example function to deposit money into an account and log transaction
def deposit(customer_id, amount):
    # Example: Log transaction to file
    transaction_log_file = os.path.join(TRANSACTIONS_DIR, f"transaction_log_{datetime.now().strftime('%Y-%m-%d')}.txt")
    with open(transaction_log_file, 'a') as file:
        file.write(f"{datetime.now()},{customer_id},Deposit,{amount}\n")

    # Example: Update account balance in 'accounts.txt'
    update_account_balance(customer_id, amount)

# Example function to withdraw money from an account and log transaction
def withdraw(customer_id, amount):
    # Example: Log transaction to file
    transaction_log_file = os.path.join(TRANSACTIONS_DIR, f"transaction_log_{datetime.now().strftime('%Y-%m-%d')}.txt")
    with open(transaction_log_file, 'a') as file:
        file.write(f"{datetime.now()},{customer_id},Withdrawal,{amount}\n")

    # Example: Update account balance in 'accounts.txt'
    update_account_balance(customer_id, -amount)  # Use negative amount for withdrawal

# Example function to update account balance in 'accounts.txt'
def update_account_balance(customer_id, amount):
    # Example: Read current account details from file, update balance, and rewrite file
    updated_lines = []
    with open(ACCOUNTS_FILE, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if data[0] == customer_id:
                current_balance = float(data[2])
                new_balance = current_balance + amount
                updated_lines.append(f"{data[0]},{data[1]},{new_balance}\n")
            else:
                updated_lines.append(line)
    
    # Rewrite 'accounts.txt' with updated balances
    with open(ACCOUNTS_FILE, 'w') as file:
        file.writelines(updated_lines)

# Example function to generate statement of account for a customer
def generate_statement_of_account(customer_id, start_date, end_date):
    # Validate date format
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    # Example: Retrieve transactions within the specified date range from transaction logs
    transactions = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    for log_file in os.listdir(TRANSACTIONS_DIR):
        log_date_str = log_file.replace("transaction_log_", "").replace(".txt", "")
        log_date = datetime.strptime(log_date_str, "%Y-%m-%d")
        if start_date_obj <= log_date <= end_date_obj:
            with open(os.path.join(TRANSACTIONS_DIR, log_file), 'r') as file:
                for line in file:
                    transaction_date, transaction_customer_id, transaction_type, transaction_amount = line.strip().split(',')
                    if transaction_customer_id == customer_id:
                        transactions.append(f"{transaction_date},{transaction_type},${transaction_amount}")

    # Example: Calculate total deposits and withdrawals
    total_deposits = sum(float(t.split(',')[2]) for t in transactions if t.split(',')[1] == 'Deposit')
    total_withdrawals = sum(float(t.split(',')[2]) for t in transactions if t.split(',')[1] == 'Withdrawal')

    # Example: Print statement of account
    print(f"Statement of Account for Customer ID: {customer_id}")
    print(f"Period: {start_date} to {end_date}")
    print("Transactions:")
    for transaction in transactions:
        print(transaction)
    print(f"Total Deposits: ${total_deposits}")
    print(f"Total Withdrawals: ${total_withdrawals}")

# Entry point of the application
if __name__ == "__main__":
    initialize()  # Initialize application (load data)


# elif choice == '2':
        #     name = input("Enter customer's name: ")
        #     dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
        #     while not validate_date_format(dob):
        #         print("Invalid date format. Please enter date in the format YYYY-MM-DD.")
        #         dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
        #     account_type = input("Enter account type (savings/current): ").lower()
        #     account_number, message = register_customer(name, dob, account_type)
            
        #     if account_number:
        #         print(f"Customer registered successfully. Account Number: {account_number}, Password: {message}") 
        #     else:
        #         print(f"Error: {message}") 
        #     break