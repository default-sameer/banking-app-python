import os
from utils.constants import CUSTOMERS_FILE

def generate_unique_customer_id():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as file:
            lines = file.readlines()
            if len(lines) == 0:
                return 1
            last_line = lines[-1]
            last_customer_id = int(last_line.split(",")[0])
            return last_customer_id + 1
    return 1

# generate unique account number
def generate_unique_account_number():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as file:
            lines = file.readlines()
            if len(lines) == 0:
                return 1001
            last_line = lines[-1]
            last_account_number = int(last_line.split(",")[4])
            return last_account_number + 1
    return 1001
