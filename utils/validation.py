from datetime import datetime

def validate_date_format(date_string):
    try:
        # Attempt to parse the date string according to the format YYYY-MM-DD
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_account_type(account_type):
    if account_type.lower() not in ['savings', 'current']:
        return False
    return True