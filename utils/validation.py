from datetime import datetime

def validate_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_account_type(account_type):
    if account_type.lower() not in ['savings', 'current']:
        return False
    return True

def get_account_number_and_dob():
    account_number = input("Enter account number: ")
    dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
    while not validate_date_format(dob):
        print("Invalid date format. Please enter date in the format YYYY-MM-DD.")
        dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
    return account_number, dob