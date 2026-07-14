import streamlit as st
import auth
import utils
import database
import config
from PIL import Image
import os

# Load style modifications
utils.load_css()

# Safety redirect if not authenticated
if not auth.is_authenticated():
    st.switch_page("app.py")

# Fetch logged-in user
user = auth.get_logged_in_user()
user_id = user.get("id")

# Header
utils.gradient_title("👤 Personal Profile Settings", "Manage your account identity, security, and avatar photo.")

# Create columns for styling
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### Profile Avatar")
    avatar_file = config.ASSETS_DIR / f"avatar_{user_id}.png"
    
    # Display avatar
    if avatar_file.exists():
        st.image(str(avatar_file), width=180)
    else:
        st.image(str(config.LOGO_PATH), width=180)
        
    uploaded_file = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        try:
            # Process avatar with Pillow
            img = Image.open(uploaded_file)
            # Crop/Resize to square format 200x200
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            # Save file
            img.save(avatar_file, "PNG")
            st.success("Profile photo uploaded successfully!")
            st.toast("Profile photo updated!", icon="📸")
            st.rerun()
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

with col2:
    st.markdown("### Account Credentials")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Read-only information
        st.text_input("Email Address (Primary)", value=user.get("email"), disabled=True)
        st.text_input("User Access Role", value=str(user.get("role")).upper(), disabled=True)
        
        # Modifiable name field
        new_name = st.text_input("Display Name", value=user.get("name"))
        
        # Password adjustment fields
        st.markdown("---")
        st.markdown("#### Change Password")
        new_pw = st.text_input("New Password", type="password", placeholder="Leave blank to keep current password")
        confirm_pw = st.text_input("Confirm New Password", type="password", placeholder="Leave blank to keep current password")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Save Action
    if st.button("💾 Save Profile Changes"):
        # Validations
        if not new_name.strip():
            utils.alert("Display Name cannot be empty.", "danger")
        elif new_pw or confirm_pw:
            if new_pw != confirm_pw:
                utils.alert("Passwords do not match.", "danger")
            elif len(new_pw) < 6:
                utils.alert("Password should be at least 6 characters long.", "danger")
            else:
                # Update user with name and password
                updated = database.update_user(user_id, name=new_name, password=new_pw)
                if updated:
                    # Sync session state
                    session_user = {k: v for k, v in updated.items() if k != "password"}
                    st.session_state.user = session_user
                    st.success("Profile and password updated successfully!")
                    st.toast("Profile saved!", icon="💾")
                    st.rerun()
        else:
            # Update user with name only
            updated = database.update_user(user_id, name=new_name)
            if updated:
                # Sync session state
                session_user = {k: v for k, v in updated.items() if k != "password"}
                st.session_state.user = session_user
                st.success("Profile updated successfully!")
                st.toast("Profile saved!", icon="💾")
                st.rerun()
