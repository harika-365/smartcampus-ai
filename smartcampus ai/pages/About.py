import streamlit as st
import auth
import utils

# Load style configurations
utils.load_css()

# Redirect to home if not authenticated
if not auth.is_authenticated():
    st.switch_page("app.py")

user = auth.get_logged_in_user()

# Header
utils.gradient_title("ℹ️ About SmartCampus AI", "Enterprise-ready AI assistant and metrics platform for smart universities.")

# Main content layout
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### 🏫 Platform Vision")
    st.write("""
    SmartCampus AI bridges the gap between modern academic administration and Artificial Intelligence. By consolidating classroom data, course analytics, and LLM-driven research utilities under a secure, single-sign-on panel, we enable students, professors, and administrators to work and learn more effectively.
    
    The application leverages high-performance Python engines, asynchronous rendering schemas, and secure JSON databases to deliver sub-millisecond local latency with military-grade safety practices.
    """)
    
    st.markdown("### ✨ Key Features Showcase")
    st.write("""
    - **🔑 Secure Authentication Layer**: Enterprise-level password security leveraging `bcrypt` and Streamlit state parameters.
    - **🤖 OpenAI Integrations**: Instant connection to advanced GPT models with full Markdown, Python code rendering, and custom prompt memory.
    - **📊 Plotly Data Analytics**: Custom interactive panels monitoring attendance behaviors, login histories, student demographics, and campus trends.
    - **⚙️ High-Fidelity Configurations**: Granular user themes, notification settings, and session profile storage modules.
    - **📱 Unified Design Standards**: Premium responsive glassmorphic interfaces, hover effects, CSS custom fonts, and multi-device compatibilities.
    """)

with col2:
    st.markdown("### 🛠️ Platform Specifications")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("**Core Engine:** Python 3.11+")
        st.write("**UI Framework:** Streamlit (v1.35.0+)")
        st.write("**Database Engine:** Modular JSON DB")
        st.write("**Hasing Protocol:** Blowfish Hashing (Bcrypt)")
        st.write("**Visual Framework:** Plotly Express & Pandas")
        st.write("**Version:** 1.0.0 (Production Release)")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("### 🎓 Developer Credits")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("Developed by **SmartCampus AI Team**")
        st.write("Support: [support@smartcampus.ai](mailto:support@smartcampus.ai)")
        st.write("Licence: MIT Academic License")
        st.markdown('</div>', unsafe_allow_html=True)
