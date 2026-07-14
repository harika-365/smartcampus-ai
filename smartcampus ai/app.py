import streamlit as st
import auth
import utils
import config

# Set page config FIRST
st.set_page_config(
    page_title="SmartCampus AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS styles
utils.load_css()
utils.generate_default_assets()

# Initialize session
auth.init_session()

def login_page_func():
    """Renders the login view."""
    st.markdown('<div class="logo-container" style="text-align:center;">', unsafe_allow_html=True)
    if config.LOGO_PATH.exists():
        st.image(str(config.LOGO_PATH), width=90)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center; font-family: Outfit; font-weight: 700; color: #1e3c72; margin-bottom: 25px;">Sign In to SmartCampus AI</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            email = st.text_input("Email Address", placeholder="e.g. admin@smartcampus.ai")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            remember_me = st.checkbox("Remember Login")
            
            if st.button("Sign In"):
                if not email.strip() or not password.strip():
                    utils.alert("Please fill in all fields.", "danger")
                else:
                    if auth.login_user(email, password):
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        utils.alert("Invalid email or password.", "danger")
            st.markdown('</div>', unsafe_allow_html=True)

def register_page_func():
    """Renders the registration view."""
    st.markdown('<div class="logo-container" style="text-align:center;">', unsafe_allow_html=True)
    if config.LOGO_PATH.exists():
        st.image(str(config.LOGO_PATH), width=90)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center; font-family: Outfit; font-weight: 700; color: #1e3c72; margin-bottom: 25px;">Create Account</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="e.g. John Doe")
            email = st.text_input("Email Address", placeholder="e.g. john@smartcampus.ai")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            role = st.selectbox("Role", options=["student", "faculty", "admin"])
            
            if st.button("Sign Up"):
                if not name.strip() or not email.strip() or not password.strip() or not confirm_password.strip():
                    utils.alert("Please fill in all fields.", "danger")
                elif password != confirm_password:
                    utils.alert("Passwords do not match.", "danger")
                else:
                    success, msg = auth.register_user(name, email, password, role)
                    if success:
                        st.success(msg)
                        st.balloons()
                    else:
                        utils.alert(msg, "danger")
            st.markdown('</div>', unsafe_allow_html=True)

def logout_page_func():
    """Renders logout action."""
    auth.logout_user()
    st.rerun()

# Build Navigation
if not auth.is_authenticated():
    # Unauthenticated navigation options
    pages = [
        st.Page(login_page_func, title="Login", icon="🔒"),
        st.Page(register_page_func, title="Register", icon="📝"),
    ]
else:
    # Authenticated navigation options
    pages = [
        st.Page("pages/Dashboard.py", title="Dashboard", icon="🏠", default=True),
        st.Page("pages/AI_Assistant.py", title="AI Assistant", icon="🤖"),
        st.Page("pages/Analytics.py", title="Analytics", icon="📊"),
        st.Page("pages/Profile.py", title="Profile", icon="👤"),
        st.Page("pages/Settings.py", title="Settings", icon="⚙️"),
        st.Page("pages/About.py", title="About", icon="ℹ️"),
        st.Page(logout_page_func, title="Logout", icon="🚪"),
    ]

# Create Sidebar Navigation Menu
pg = st.navigation(pages)
pg.run()
