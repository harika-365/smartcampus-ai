import streamlit as st
import auth
import utils
import database
import config

# Load style modifications
utils.load_css()

# Safety Redirect: If not authenticated, redirect to app.py
if not auth.is_authenticated():
    st.switch_page("app.py")

# Get authenticated user info
user = auth.get_logged_in_user()

# Header banner
utils.gradient_title(f"Welcome, {user.get('name')}!", f"Role: {str(user.get('role')).capitalize()} | Account Center")

# Create layout: Left column (Profile & Actions), Right column (Stats & Logs)
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 👤 User Profile Card")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Profile avatar
        avatar_path = config.ASSETS_DIR / f"avatar_{user.get('id')}.png"
        if avatar_path.exists():
            st.image(str(avatar_path), width=100)
        else:
            # Fallback logo
            st.image(str(config.LOGO_PATH), width=100)
            
        st.markdown(f"**Name:** {user.get('name')}")
        st.markdown(f"**Email:** {user.get('email')}")
        st.markdown(f"**Role:** {str(user.get('role')).upper()}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Actions")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.button("🤖 Launch AI Assistant", key="qa_ai"):
            st.switch_page("pages/AI_Assistant.py")
        st.write("")
        if st.button("📊 View Analytics Dashboard", key="qa_analytics"):
            st.switch_page("pages/Analytics.py")
        st.write("")
        if st.button("⚙️ Customize Settings", key="qa_settings"):
            st.switch_page("pages/Settings.py")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 📈 Campus Analytics Overview")
    
    # 2x2 grid for metrics
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        utils.card("Total Student Enrollment", "1,240 students", "Active this semester", "#1e90ff")
    with m_col2:
        utils.card("Faculty & Instructors", "84 professors", "Across 6 departments", "#1e3c72")
        
    m_col3, m_col4 = st.columns(2)
    with m_col3:
        # Load user settings to see if they customized model or check defaults
        settings = database.load_json(config.SETTINGS_DB_PATH)
        selected_model = settings.get("default_model", config.DEFAULT_MODEL)
        utils.card("AI Assist Queries", "14,802 runs", f"Model: {selected_model}", "#10b981")
    with m_col4:
        utils.card("Average Campus Attendance", "94.2%", "Target: 95.0%", "#f59e0b")

    st.markdown("### 🔔 Active System Notifications")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.info("📢 Course registration period for Fall 2026 is officially open until July 31st.")
        st.warning("⚠️ Scheduled network maintenance: Saturday from 02:00 AM to 05:00 AM. Internet access may be unstable.")
        st.success("🎓 SmartCampus AI API modules updated: response latency reduced by 15%.")
        st.markdown('</div>', unsafe_allow_html=True)

# Recent Activity Log section at the bottom
st.markdown("### 🕒 Your Recent Activities")
logs = database.load_json(config.LOGS_DB_PATH)
user_logs = [l for l in logs if l.get("user_id") == user.get("id")]
# Sort logs by timestamp descending
user_logs = sorted(user_logs, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]

if user_logs:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for log in user_logs:
        st.write(f"⏱️ **{log.get('timestamp')}** - **{log.get('action')}**: {log.get('details')}")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("No logged activities found for your profile.")
