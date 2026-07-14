import streamlit as st
import pandas as pd
import plotly.express as px
import auth
import utils

# Load custom CSS styles
utils.load_css()

# Safety redirect if user is not authenticated
if not auth.is_authenticated():
    st.switch_page("app.py")

user = auth.get_logged_in_user()

# Header
utils.gradient_title("📊 SmartCampus Analytics Hub", "Real-time administrative charts and usage statistics.")

# Filter Sidebar Options
st.sidebar.markdown("### 🔍 Analytics Filters")
selected_dept = st.sidebar.selectbox("Filter Department data:", ["All Departments", "Computer Science", "Electrical Eng", "Mechanical Eng", "Business", "Humanities"])
selected_timeframe = st.sidebar.radio("Timeframe Selection:", ["This Semester", "Previous Semester", "Full Academic Year"])

# Metrics Summary Bar
st.markdown("### 📈 Quick Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    utils.card("Total Active Students", "1,540", "📊 +4.2% from last term", "#1e90ff")
with col2:
    utils.card("Total Active Faculty", "87", "🧑‍🏫 Ratio 1:17", "#1e3c72")
with col3:
    utils.card("Average Attendance Rate", "94.2%", "📈 Target is 95%", "#10b981")
with col4:
    utils.card("Total AI Requests", "14,802 runs", "🤖 98.6% success rate", "#f59e0b")

# Sample Data Initializations
# 1. Departments Data (Students vs Faculty)
dept_data = {
    "Department": ["Computer Science", "Electrical Eng", "Mechanical Eng", "Business", "Humanities"],
    "Students": [450, 320, 240, 350, 180],
    "Faculty": [25, 18, 14, 20, 10]
}
df_dept = pd.DataFrame(dept_data)

# Apply simple filter if department is selected
if selected_dept != "All Departments":
    df_dept = df_dept[df_dept["Department"] == selected_dept]

# 2. AI Usage Breakdown Data
ai_data = {
    "Feature": ["Coding Assistant", "Homework Helper", "Research Summarizer", "Schedule Planner", "GPA Calculator"],
    "Requests": [4200, 3100, 3500, 2500, 1502]
}
df_ai = pd.DataFrame(ai_data)

# 3. Monthly Activity Data
activity_data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Logins": [1200, 2100, 2900, 2700, 3300, 4100],
    "AI Queries": [800, 1500, 2400, 2200, 3800, 4102]
}
df_activity = pd.DataFrame(activity_data)

# 4. Weekly Attendance Rate (%) Data
attendance_data = {
    "Week": [f"Week {i}" for i in range(1, 9)],
    "Attendance": [95.2, 94.8, 93.9, 94.5, 95.1, 93.2, 94.0, 94.2]
}
df_attendance = pd.DataFrame(attendance_data)

# Visual layout using tabs
tab1, tab2 = st.tabs(["🏛️ Department & Attendance Analytics", "🤖 AI Assistant & Activity Trends"])

with tab1:
    st.write("")
    chart_col1, chart_col2 = st.columns(2, gap="medium")
    
    with chart_col1:
        st.markdown("#### Student and Faculty Count by Department")
        # Bar Chart
        df_melted = df_dept.melt(id_vars="Department", value_vars=["Students", "Faculty"], var_name="Role", value_name="Count")
        fig_bar = px.bar(
            df_melted,
            x="Department",
            y="Count",
            color="Role",
            barmode="group",
            color_discrete_map={"Students": "#1e90ff", "Faculty": "#1e3c72"},
            template="plotly_white"
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with chart_col2:
        st.markdown("#### Attendance Trend Over Current Semester")
        # Area Chart
        fig_area = px.area(
            df_attendance,
            x="Week",
            y="Attendance",
            line_shape="spline",
            color_discrete_sequence=["#1e90ff"],
            labels={"Attendance": "Attendance Rate (%)"},
            template="plotly_white"
        )
        # Set range for attendance to make variations visible but clear
        fig_area.update_yaxes(range=[90, 100])
        fig_area.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_area, use_container_width=True)

with tab2:
    st.write("")
    chart_col3, chart_col4 = st.columns(2, gap="medium")
    
    with chart_col3:
        st.markdown("#### AI Assistant Queries Breakdown")
        # Pie Chart
        fig_pie = px.pie(
            df_ai,
            values="Requests",
            names="Feature",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4,
            template="plotly_white"
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with chart_col4:
        st.markdown("#### Monthly Platform Logins & AI Queries")
        # Line Chart
        fig_line = px.line(
            df_activity,
            x="Month",
            y=["Logins", "AI Queries"],
            markers=True,
            line_shape="linear",
            color_discrete_map={"Logins": "#1e3c72", "AI Queries": "#10b981"},
            template="plotly_white"
        )
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_line, use_container_width=True)

# Full summary card at the bottom
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("##### 💡 Analytics Key Findings")
st.write("""
- **AI Assist queries** have grown exponentially by **24%** since April, correlating with midterm review cycles.
- **Computer Science** remains the largest department with a 1:18 faculty-to-student ratio.
- The average student attendance rate holds stable around **94.2%**, with minor dips observed during Week 6 (project submission week).
""")
st.markdown('</div>', unsafe_allow_html=True)
