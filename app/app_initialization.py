import os
from utils.constants import DATA_DIR, TRANSACTIONS_DIR
from utils.helpers import create_super_user

def initialize_app():
    if not os.path.exists(DATA_DIR):
        print('Creating data directory. Please wait...')
        os.makedirs('data')
    
    if not os.path.exists(TRANSACTIONS_DIR):
        print('Creating transactions directory. Please wait...')
        os.makedirs(TRANSACTIONS_DIR)
    

    create_super_user()