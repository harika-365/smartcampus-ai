# SmartCampus AI - Intelligent Academic Hub

SmartCampus AI is a modern, production-ready campus management, administrative analytics, and AI-driven study assistant platform. Engineered using Python, Streamlit, and standard security guidelines, this application equips students and faculty with key widgets, visual insights, and interactive chatbot services.

## 🚀 Key Features

* **🛡️ Modern Authentication**: Encrypted credentials stored using `bcrypt` blowfish hashing. Standard login, user registration, logout, and session safety are built natively.
* **🏠 Personalized Dashboard**: Responsive statistics grids, recent logs, smart notices, profile summaries, and quick navigation keys.
* **🤖 AI Assistant Integration**: Interactive chat panels powered by OpenAI's completions SDK. Features syntax highlighted code blocks, markdown representation, conversation clearing, and customizable session-level keys.
* **📊 Analytics Hub**: Dynamic Plotly graphs charting department populations (students vs faculty), semester attendance, platform logins, and query ratios.
* **👤 Account Profile Management**: Secure name modifications, password updates, and avatar uploads (powered by PIL processing).
* **⚙️ System Configuration**: Custom theme settings, model toggling, notification permission controls, and sidebar preferences.
* **📁 Auto-initializing Database**: Complete local resilience using safe JSON databases that initialize automatically on start.

---

## 📂 Project Directory Structure

```text
smartcampus-ai/
│
├── app.py                  # Main router and navigation entrypoint
├── requirements.txt        # Python dependency packages list
├── .env                    # Active local environment variables
├── .env.example            # Environment variables template
├── config.py               # Constants, base paths, and directory managers
├── auth.py                 # Password hashing, validation, and session states
├── database.py             # JSON DB reading/writing operations & logs
├── utils.py                # CSS injections, visual cards, and default assets
│
├── assets/
│   ├── logo.png            # Application logo image (auto-generated)
│   ├── styles.css          # Custom styling and glassmorphism overrides
│   └── background.jpg      # Dynamic canvas background (auto-generated)
│
├── data/
│   ├── users.json          # Encrypted accounts storage
│   ├── logs.json           # User activity logger
│   └── settings.json       # App configuration parameters
│
├── pages/
│   ├── Dashboard.py        # Landing panel and user metrics
│   ├── Profile.py          # User details and password changer
│   ├── AI_Assistant.py     # OpenAI assistant chat interface
│   ├── Analytics.py        # Plotly charts and demographics
│   ├── Settings.py         # Preferences editor
│   └── About.py            # Platform developer information
│
└── README.md               # Setup and usage guide
```

---

## 🛠️ Local Installation & Setup

Follow these simple steps to run SmartCampus AI on your machine:

### 1. Prerequisite Checks
Make sure you have **Python 3.11+** installed. You can check your version by running:
```bash
python --version
```

### 2. Configure Virtual Environment
We recommend deploying inside a virtual environment:
```bash
# Create a virtual environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate.bat

# Activate on Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Run the install command using our pinned stable versions:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Duplicate the `.env.example` file to create your active `.env`:
```bash
cp .env.example .env
```
Open the `.env` file and input your settings:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
APP_NAME=SmartCampus AI
SECRET_KEY=enter_any_custom_secure_key
```
*Note: If you do not have an OpenAI API Key handy, the AI Assistant page includes a field inside the sidebar to input a temporary session key directly from your browser!*

### 5. Running the Application
Launch the Streamlit server using:
```bash
streamlit run app.py
```
The application will spin up locally and load in your browser at `http://localhost:8501`.

---

## 🔓 Default Login Credentials
Upon initial start, the JSON database initializes automatically with a default administrative profile:
- **Email:** `admin@smartcampus.ai`
- **Password:** `admin123`

You can use these credentials to sign in immediately, update details inside the **Profile** screen, and create new student/faculty accounts using the **Register** menu.

---

## ☁️ Production Deployment

SmartCampus AI runs securely on multiple cloud providers:

### Streamlit Community Cloud
1. Push your repository to GitHub.
2. Visit [Streamlit Share](https://share.streamlit.io/).
3. Connect your repository, set the entry point file to `app.py`, and paste your `.env` contents into the Streamlit dashboard **Secrets** field.

### Render, Railway, or Replit
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
* Inject variables (`OPENAI_API_KEY`, `APP_NAME`, `SECRET_KEY`) under the Environment configuration tab in your dashboard.
