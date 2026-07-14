import json
import os
import bcrypt
from datetime import datetime
from config import USERS_DB_PATH, SETTINGS_DB_PATH, LOGS_DB_PATH

def load_json(file_path):
    """Loads JSON data from file. Safe from corruption, missing files, and empty files."""
    if not os.path.exists(file_path):
        # Initialise standard file layout
        if "settings.json" in str(file_path):
            return {}
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                if "settings.json" in str(file_path):
                    return {}
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        # Recovery/corrupted file scenario
        print(f"Error loading JSON from {file_path}: {e}")
        if "settings.json" in str(file_path):
            return {}
        return []

def save_json(file_path, data):
    """Saves data back to file in JSON format."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error writing JSON to {file_path}: {e}")
        return False

def init_db():
    """Initializes the files in database folder if missing or corrupted."""
    # Ensure folder is created
    os.makedirs(os.path.dirname(USERS_DB_PATH), exist_ok=True)
    
    # Initialize users DB with a default admin user
    if not os.path.exists(USERS_DB_PATH) or os.path.getsize(USERS_DB_PATH) == 0:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw("admin123".encode('utf-8'), salt).decode('utf-8')
        default_users = [
            {
                "id": 1,
                "name": "Admin User",
                "email": "admin@smartcampus.ai",
                "password": hashed,
                "role": "admin"
            }
        ]
        save_json(USERS_DB_PATH, default_users)
        
    # Initialize settings DB
    if not os.path.exists(SETTINGS_DB_PATH) or os.path.getsize(SETTINGS_DB_PATH) == 0:
        default_settings = {
            "theme": "Blue/White",
            "notifications": True,
            "default_model": "gpt-4o-mini",
            "sidebar_option": "Expanded"
        }
        save_json(SETTINGS_DB_PATH, default_settings)

    # Initialize logs DB
    if not os.path.exists(LOGS_DB_PATH) or os.path.getsize(LOGS_DB_PATH) == 0:
        save_json(LOGS_DB_PATH, [])

def create_user(name, email, password, role="student"):
    """Creates a new user and stores user details inside users.json."""
    users = load_json(USERS_DB_PATH)
    if not isinstance(users, list):
        users = []
        
    # Normalise email
    email = email.strip().lower()
    
    # Check duplicate email
    for user in users:
        if user.get("email") == email:
            raise ValueError("A user with this email address already exists.")
            
    # Hash password using bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    next_id = max([u.get("id", 0) for u in users], default=0) + 1
    new_user = {
        "id": next_id,
        "name": name.strip(),
        "email": email,
        "password": hashed_password,
        "role": role
    }
    users.append(new_user)
    save_json(USERS_DB_PATH, users)
    
    # Log registration activity
    log_activity(next_id, "Register", f"Successfully registered user: {email} ({role})")
    return new_user

def authenticate_user(email, password):
    """Authenticates credentials against database. Returns user dict or None."""
    users = load_json(USERS_DB_PATH)
    if not isinstance(users, list):
        return None
        
    email = email.strip().lower()
    for user in users:
        if user.get("email") == email:
            hashed_pw = user.get("password")
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
                log_activity(user["id"], "Login", "Successfully logged in")
                return user
    return None

def update_user(user_id, name=None, password=None, role=None, additional_data=None):
    """Updates user configurations inside JSON database."""
    users = load_json(USERS_DB_PATH)
    if not isinstance(users, list):
        return None
        
    updated_user = None
    for user in users:
        if user.get("id") == user_id:
            if name is not None:
                user["name"] = name.strip()
            if role is not None:
                user["role"] = role
            if password is not None and password.strip() != "":
                salt = bcrypt.gensalt()
                user["password"] = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            if additional_data is not None:
                for k, v in additional_data.items():
                    user[k] = v
            updated_user = user
            break
            
    if updated_user:
        save_json(USERS_DB_PATH, users)
        log_activity(user_id, "Profile Update", "Profile information was updated")
    return updated_user

def delete_user(user_id):
    """Deletes user from users.json."""
    users = load_json(USERS_DB_PATH)
    if not isinstance(users, list):
        return False
        
    initial_length = len(users)
    users = [u for u in users if u.get("id") != user_id]
    if len(users) < initial_length:
        save_json(USERS_DB_PATH, users)
        log_activity(user_id, "Delete Account", "User account was deleted")
        return True
    return False

def log_activity(user_id, action, details):
    """Appends action to logs.json."""
    logs = load_json(LOGS_DB_PATH)
    if not isinstance(logs, list):
        logs = []
        
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "action": action,
        "details": details
    }
    logs.append(log_entry)
    
    # Cap size to last 500 rows to optimize file sizing
    if len(logs) > 500:
        logs = logs[-500:]
        
    save_json(LOGS_DB_PATH, logs)
