from app.session import is_session_expired, save_session

def handle_session_timeout(session):
    if is_session_expired(session):
        print("Session has expired. Please log in again.")
        session.clear()
        save_session(session)
        return True
    return False