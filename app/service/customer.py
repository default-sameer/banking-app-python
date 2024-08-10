
from datetime import datetime
import os
from utils.constants import CUSTOMERS_FILE, ACCOUNTS_FILE, TRANSACTIONS_DIR, TRANSACTION_FILE

def load_customer_data():
    customers = []
    with open(CUSTOMERS_FILE, 'r') as file:
        for line in file:
            customer_id, name, dob, account_type, account_number, password, created_by = line.strip().split(',')
            customers.append({'customer_id': customer_id, 'name': name, 'dob': dob, 'account_type': account_type, 'account_number': account_number, 'password': password, 'created_by' : created_by})
    return customers

def delete_customer_account(account_number, dob):
    customers = load_customer_data()
    customer_found = False

    for data in customers:
        if data['account_number'] == account_number and data['dob'] == dob:
            customers.remove(data)
            customer_found = True
            break

    if customer_found:
        with open(CUSTOMERS_FILE, 'w') as file:
            for customer in customers:
                file.write(f"{customer['customer_id']},{customer['name']},{customer['dob']},{customer['account_type']},{customer['account_number']},{customer['password']},{customer['created_by']}\n")
        
        with open(ACCOUNTS_FILE, 'r') as file:
            accounts = file.readlines()

        with open(ACCOUNTS_FILE, 'w') as file:
            for account in accounts:
                account_data = account.strip().split(',')
                if account_data[2].strip() != account_number:
                    file.write(account)
        
        with open(ACCOUNTS_FILE, 'r') as file:
            accounts = file.readlines()
            for account in accounts:
                account_data = account.strip().split(',')
                if account_data[2].strip() == account_number:
                    return False, "Failed to delete customer account from ACCOUNTS_FILE."

        return True, "Customer account deleted successfully."
    else:
        return False, "Customer account not found."
    
def edit_customer_account_type(account_number, dob, new_account_type):
    customers = load_customer_data()
    customer_found = False

    for data in customers:
        if data['account_number'] == account_number and data['dob'] == dob:
            data['account_type'] = new_account_type
            customer_found = True
            break

    if customer_found:
        with open(CUSTOMERS_FILE, 'w') as file:
            for customer in customers:
                file.write(f"{customer['customer_id']},{customer['name']},{customer['dob']},{customer['account_type']},{customer['account_number']},{customer['password']},{customer['created_by']}\n")
        return True, "Customer account type updated successfully."
    else:
        return False, "Customer account not found."
    

def check_available_balance(account_number):
    with open(ACCOUNTS_FILE, 'r') as file:
        accounts = file.readlines()

    for account in accounts:
        account_data = account.strip().split(',')
        if account_data[2].strip() == account_number:
            balance = account_data[4].strip()
            return True, f"Available balance: {balance}"

    return False, "Account not found." 

def update_account_balance(account_number, amount, transaction_type):
    with open(ACCOUNTS_FILE, 'r') as file:
        accounts = file.readlines()

    account_found = False
    updated_accounts = []
    account_name = ""

    for account in accounts:
        account_data = account.strip().split(',')
        if account_data[2].strip() == account_number:
            account_name = account_data[1].strip()
            account_type = account_data[3].strip()
            current_balance = float(account_data[4].strip())
            amount = float(amount)

            if transaction_type == 'withdraw':
                new_balance = current_balance - amount
                if account_type == 'savings' and new_balance < 100:
                    return False, "Insufficient funds. Minimum balance for savings account is 100."
                elif account_type == 'current' and new_balance < 500:
                    return False, "Insufficient funds. Minimum balance for current account is 500."
                elif new_balance < 0:
                    return False, "Insufficient funds for withdrawal."
            elif transaction_type == 'deposit':
                new_balance = current_balance + amount
            else:
                return False, "Invalid transaction type."

            account_data[4] = str(new_balance)
            account_found = True

        updated_accounts.append(','.join(account_data) + '\n')

    if account_found:
        with open(ACCOUNTS_FILE, 'w') as file:
            file.writelines(updated_accounts)
        
        # Log the transaction
        log_transaction(account_number, account_name, amount, transaction_type)
        
        return True, "Account balance updated successfully."
    else:
        return False, "Account not found."

def log_transaction(account_number, account_name, amount, transaction_type):
    if not os.path.exists(TRANSACTIONS_DIR):
        os.makedirs(TRANSACTIONS_DIR)
    
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, 'w') as file:
            file.write("account_number,account_name,amount,transaction_type,transaction_time\n")
    
    with open(TRANSACTION_FILE, 'a') as file:
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{account_number},{account_name},{amount},{transaction_type},{transaction_time}\n")