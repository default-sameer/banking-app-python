from datetime import datetime
import os
from app.session import save_session, update_last_activity
from utils.constants import USERS_FILE
import getpass
from utils.session_helpers import handle_session_timeout
from utils.customer_helpers import handle_customer_tasks

# def create_users_file_if_not_exists():
#     if not os.path.exists(USERS_FILE):
#         with open(USERS_FILE, 'w') as file:
#             print("Users file created successfully.")

def create_users_file_if_not_exists():
    try:
        open(USERS_FILE, 'x').close()
    except FileExistsError:
        pass
            
def display_logged_in_user(session):
    if 'role' in session:
       print(f"\nLogged in: {session['username']} as {session['role']}")
    elif 'customer' in session:
        print(f"\nLogged in as: {session['customer']}")
        
def load_users():
    users = []
    create_users_file_if_not_exists()
    with open(USERS_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                username, password, role, last_login = parts
                users.append({'username': username, 'password': password, 'role': role, 'last_login': last_login})
            else:
                print(f"Skipping invalid line in users file: {line.strip()}")
    return users

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        for user in users:
            file.write(f"{user['username']},{user['password']},{user['role']},{user['last_login']}\n")

def user_login():
    username_input = input("Enter your username: ")
    password_input = getpass.getpass("Enter your password: ")


    users = load_users()

    for user in users:
        if user['username'] == username_input and user['password'] == password_input:
            print("Login successful!")
            return user['role']  # Return the role of the user
    print("Invalid username or password.")
    return None

def handle_user_login(session):
    user_role = user_login()
    if user_role == "superadmin":
        session['role'] = 'superadmin'
        session = update_last_activity(session)
        print("Welcome, Super Admin!")
        handle_superadmin_tasks(session)
    elif user_role:
        session['role'] = 'user'
        session = update_last_activity(session)
        print("Welcome, User!")
        handle_user_tasks(session)


def handle_superadmin_tasks(session):
    while True:
        if handle_session_timeout(session):
            break
        # print(f"\nLogged in: {session['username']} as {session['role']}")
        display_logged_in_user(session)
        print("1. Create User")
        print("2. Change Username")
        print("3. Change Password")
        print("4. Logout")
        admin_choice = input("Enter your choice: ")
        session = update_last_activity(session)
        if admin_choice == '1':
            create_user()
        elif admin_choice == '2':
            change_username(session)
        elif admin_choice == '3':
            change_password(session)
        elif admin_choice == '4':
            print("Logging out...")
            session.clear()
            save_session(session)
            return
        else:
            print("Invalid choice. Please try again.")
            
        
def handle_user_tasks(session):
    while True:
        if handle_session_timeout(session):
            break
        print("\nUser Menu:")
        print("1. Change Username")
        print("2. Change Password")
        print("3. View Customer Portal")
        print("4. Logout")
        user_choice = input("Enter your choice: ")
        session = update_last_activity(session)
        if user_choice == '1':
            change_username(session)
        elif user_choice == '2':
            change_password(session)
        elif user_choice == '3':
            handle_customer_tasks(session)
        elif user_choice == '4':
            print("Logging out...")
            session.clear()
            save_session(session)
            from utils.helpers import display_main_menu
            display_main_menu(session)
            return
        else:
            print("Invalid choice. Please try again.")


def create_user():
    create_users_file_if_not_exists()
    users = load_users()
    username = input("Enter username: ")
    # Check if username already exists
    for user in users:
        if user['username'] == username:
            print(f"Username '{username}' already exists. Please choose a different username.")
            return
    
    password = getpass.getpass("Enter password: ")
    role = "user"  # Default role to "user"
    last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username},{password},{role},{last_login}\n")
    print(f"User '{username}' created successfully with role '{role}'.")

def change_username(session):
    old_username = session.get('username')
    new_username = input("Enter new username: ")
    users = load_users()
    for user in users:
        if user['username'] == old_username:
            user['username'] = new_username
            break
    save_users(users)
    session['username'] = new_username
    print(f"Username changed successfully to '{new_username}'.")

def change_password(session):
    username = session.get('username')
    new_password = getpass.getpass("Enter new password: ")
    users = load_users()
    for user in users:
        if user['username'] == username:
            user['password'] = new_password
            break
    save_users(users)
    print("Password changed successfully.")


def save_users(users):
    with open(USERS_FILE, 'w') as file:
        for user in users:
            file.write(f"{user['username']},{user['password']},{user['role']},{user['last_login']}\n")

def update_last_login(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            user['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_users(users)

def user_login():
    username_input = input("Enter your username: ")
    password_input = getpass.getpass("Enter your password: ")

    users = load_users()

    for user in users:
        if user['username'] == username_input and user['password'] == password_input:
            print("Login successful!")
            update_last_login(username_input)
            return username_input, user['role']  # Return both username and role
    print("Invalid username or password.")
    return None, None

def handle_user_login(session):
    username, user_role = user_login()
    if user_role == "superadmin":
        session['username'] = username
        session['role'] = 'superadmin'
        session = update_last_activity(session)
        print("Welcome, Super Admin!")
        handle_superadmin_tasks(session)
    elif user_role:
        session['username'] = username
        session['role'] = 'user'
        session = update_last_activity(session)
        print("Welcome, User!")
        handle_user_tasks(session)