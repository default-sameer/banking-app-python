import os
from utils.constants import DATA_DIR, TRANSACTIONS_DIR
from utils.helpers import create_super_user
from app.customer_management import load_customers, load_accounts

def initialize_app():
    if not os.path.exists(DATA_DIR):
        print('Creating data directory. Please wait...')
        os.makedirs('data')
    
    if not os.path.exists(TRANSACTIONS_DIR):
        print('Creating transactions directory. Please wait...')
        os.makedirs(TRANSACTIONS_DIR)
    
    # Load existing customer and account data into memory
    create_super_user()
    load_customers()
    load_accounts()