from datetime import datetime

def validate_date_format(date_string):
    try:
        # Attempt to parse the date string according to the format YYYY-MM-DD
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False