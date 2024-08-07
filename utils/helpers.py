

from utils.user_helpers import check_super_user_exists, create_super_user
from app.user_management import handle_superadmin_tasks, handle_user_tasks
from app.customer_management import handle_customer_tasks


def display_main_menu(session):
    if 'role' in session:
        if session['role'] == 'superadmin':
           handle_superadmin_tasks(session)
        elif session['role'] == 'user':
            handle_user_tasks(session)
        elif session['role'] == 'customer':
            handle_customer_tasks(session)
    else:
        if check_super_user_exists():
            print("\nMain Menu:")
            print("1. User Login")
            print("2. Customer Login")
            print("3. Exit")
        else:
            print("Super User account not found.")
            print("Creating Super User account with username 'admin' and password 'admin'.")
            create_super_user()
            print("\nMain Menu:")
            print("1. User Login")
            print("2. Customer Login")
            print("3. Exit")
