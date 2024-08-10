from app.session import is_session_expired, save_session

def is_customer_logging_in(session):
    return 'customer' in session and 'account_number' in session

def handle_session_timeout(session):
    if is_session_expired(session):
        print("Session has expired. Please log in again.")
        session.clear()
        save_session(session)
        return True
    return False

def handle_customer_login(session):
    if is_customer_logging_in(session):
        if 'username' in session and 'role' in session:
            print("User session found. Removing user session as customer is logging in.")
            session.pop('username', None)
            session.pop('role', None)
            save_session(session)
        print("Customer logged in successfully.")
        return True
    return False