import streamlit as st
import auth
import utils
import database
import config
from openai import OpenAI

# Load styling
utils.load_css()

# Redirect if not authenticated
if not auth.is_authenticated():
    st.switch_page("app.py")

user = auth.get_logged_in_user()

# Header
utils.gradient_title("🤖 SmartCampus AI Assistant", "Your 24/7 personal study and administrative companion.")

# Load User Preferences for the AI Model
settings = database.load_json(config.SETTINGS_DB_PATH)
selected_model = settings.get("default_model", config.DEFAULT_MODEL)

# Setup API Key (Prefer workspace .env, fallback to session-level temporary key)
api_key = st.session_state.get("temp_api_key", config.OPENAI_API_KEY)

# Sidebar configurations
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    st.info(f"🤖 Active Model: `{selected_model}`")
    
    # Custom API Key Input if missing
    if not api_key:
        st.warning("⚠️ OpenAI API Key is missing from the server `.env` file.")
        temp_key = st.text_input("Enter Temporary OpenAI API Key:", type="password")
        if temp_key:
            st.session_state.temp_api_key = temp_key
            st.toast("Temporary API Key saved for this session!", icon="🔑")
            st.rerun()
    else:
        st.success("🔑 OpenAI API Key is configured and ready.")
        
    # Clear chat button
    st.write("")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.toast("Chat history cleared!", icon="🧹")
        st.rerun()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": f"Hello {user.get('name')}! I am your SmartCampus AI assistant. I can write code, answer campus curriculum questions, analyze data, or help plan your study schedules. What can I do for you today?"
        }
    ]

# Render chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_prompt := st.chat_input("Ask a question... (e.g. Write a python script to calculate my GPA)"):
    # Display user query instantly
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Store query in session history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # Call OpenAI API
    if not api_key:
        with st.chat_message("assistant"):
            st.error("Cannot proceed: OpenAI API Key is missing. Please set it in `.env` or input it in the sidebar.")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "ERROR: OpenAI API Key was missing. Unable to complete response."
        })
    else:
        # Show a beautiful spinner while generating
        with st.spinner("Generating AI response..."):
            try:
                client = OpenAI(api_key=api_key)
                
                # Retrieve full chat context (exclude system/error statements if any)
                api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]
                
                # Fetch completion
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=api_messages,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                
                # Display response
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                
                # Store response in session history
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                # Log AI queries activity
                database.log_activity(user.get("id"), "AI Chat", f"Asked: '{user_prompt[:35]}...' | Model: {selected_model}")
                
            except Exception as e:
                error_msg = f"Failed to retrieve response from OpenAI: {str(e)}"
                with st.chat_message("assistant"):
                    st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": f"⚠️ Error: {error_msg}"})
