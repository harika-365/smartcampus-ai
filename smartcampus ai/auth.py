import streamlit as st
import database

def init_session():
    """Initializes the required session variables for login state management."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    # Initialize JSON files if missing
    database.init_db()

def is_authenticated():
    """Checks if a user is currently authenticated."""
    init_session()
    return st.session_state.authenticated

def get_logged_in_user():
    """Retrieves the currently logged-in user dict."""
    init_session()
    return st.session_state.user

def login_user(email, password):
    """Verifies credentials, records log, and sets the authenticated state."""
    init_session()
    user = database.authenticate_user(email, password)
    if user:
        st.session_state.authenticated = True
        # Keep password out of session state for safety
        session_user = {k: v for k, v in user.items() if k != "password"}
        st.session_state.user = session_user
        return True
    return False

def logout_user():
    """Clears the session and logs the user out."""
    init_session()
    user = st.session_state.user
    if user:
        database.log_activity(user.get("id"), "Logout", "User logged out")
    st.session_state.authenticated = False
    st.session_state.user = None
    st.toast("Successfully logged out!", icon="🚪")

def register_user(name, email, password, role="student"):
    """Registers a new user account with hashed password validation."""
    if not name or not email or not password:
        return False, "All fields are required."
    
    if "@" not in email or "." not in email:
        return False, "Invalid email format."
        
    try:
        database.create_user(name, email, password, role)
        return True, "Registration successful! You can now sign in."
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Registration failed: {str(e)}"
