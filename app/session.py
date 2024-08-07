import os
import time
from utils.constants import SESSION_DIR, SESSION_FILE, SESSION_TIMEOUT

def is_session_expired(session):
    if 'last_activity' in session:
        current_time = time.time()
        if current_time - session['last_activity'] > SESSION_TIMEOUT:
            return True
    return False

def update_last_activity(session):
    session['last_activity'] = time.time()
    save_session(session)
    return session

def save_session(session):
    with open(SESSION_FILE, 'w') as f:
        for key, value in session.items():
            f.write(f"{key}:{value}\n")

def load_session():
    session = {}
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)
        print(f"Session directory '{SESSION_DIR}' created.")
        
    if not os.path.exists(SESSION_FILE):
        print("Session file not found. Creating a new session file.")
        with open(SESSION_FILE, 'w') as f:
            pass  # Create an empty session file
    else:
        with open(SESSION_FILE, 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    if key == 'last_activity':
                        session[key] = float(value)
                    else:
                        session[key] = value
    return session