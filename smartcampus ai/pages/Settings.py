import streamlit as st
import auth
import utils
import database
import config

# Load style configurations
utils.load_css()

# Redirect to home if not authenticated
if not auth.is_authenticated():
    st.switch_page("app.py")

user = auth.get_logged_in_user()

# Header
utils.gradient_title("⚙️ System Preferences", "Personalize your workspace theme, notifications, and AI features.")

# Load active settings
active_settings = database.load_json(config.SETTINGS_DB_PATH)
if not isinstance(active_settings, dict):
    active_settings = {}

# Set form default values based on loaded JSON, fallback to standard configs
current_theme = active_settings.get("theme", "Blue/White")
current_notifications = active_settings.get("notifications", True)
current_model = active_settings.get("default_model", config.DEFAULT_MODEL)
current_sidebar = active_settings.get("sidebar_option", "Expanded")

# Display forms inside styled layouts
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 🖥️ Look & Feel")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        theme_val = st.selectbox(
            "Application Theme Palette:",
            options=["Blue/White", "Classic Dark", "Emerald Green", "Royal Purple"],
            index=["Blue/White", "Classic Dark", "Emerald Green", "Royal Purple"].index(current_theme) if current_theme in ["Blue/White", "Classic Dark", "Emerald Green", "Royal Purple"] else 0
        )
        
        sidebar_val = st.selectbox(
            "Default Sidebar State:",
            options=["Expanded", "Collapsed"],
            index=["Expanded", "Collapsed"].index(current_sidebar) if current_sidebar in ["Expanded", "Collapsed"] else 0
        )
        
        notify_val = st.checkbox("Enable In-App Notifications", value=current_notifications)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🧠 AI Engine Settings")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        model_val = st.selectbox(
            "Default AI Completion Model:",
            options=config.AVAILABLE_MODELS,
            index=config.AVAILABLE_MODELS.index(current_model) if current_model in config.AVAILABLE_MODELS else 0
        )
        st.info("💡 Model upgrades affect token usage limits. `gpt-4o-mini` is recommended for general speed and low API latency.")
        st.markdown('</div>', unsafe_allow_html=True)

# Submit controls
st.write("")
if st.button("💾 Save System Preferences"):
    new_settings = {
        "theme": theme_val,
        "notifications": notify_val,
        "default_model": model_val,
        "sidebar_option": sidebar_val
    }
    
    # Save preferences to JSON database
    success = database.save_json(config.SETTINGS_DB_PATH, new_settings)
    if success:
        st.success("System configurations updated successfully!")
        st.toast("Settings updated!", icon="⚙️")
        database.log_activity(user.get("id"), "Update Settings", f"Preferences: Theme={theme_val}, Model={model_val}")
        # Rerun to let changes take effect
        st.rerun()
    else:
        st.error("Failed to write configurations to database file.")
