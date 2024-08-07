import os
from datetime import datetime
from utils.constants import USERS_FILE

def create_users_file_if_not_exists():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            print("Users file created successfully.")

def create_super_user():
    if not check_super_user_exists():
        super_user = {
            "username": "sameerjoshi",
            "password": "thesuperadmin",
            "role": "superadmin",
            "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(USERS_FILE, 'a') as file:
            file.write(f"{super_user['username']},{super_user['password']},{super_user['role']},{super_user['last_login']}\n")
            print(f"Super User created successfully with username '{super_user['username']}' and password '{super_user['password']}'.")
    else:
        print("A superadmin already exists. No need to create another one.")

def check_super_user_exists():
    create_users_file_if_not_exists()
    with open(USERS_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                username, password, role, last_login = parts
                if role == "superadmin":
                    return True
    return False