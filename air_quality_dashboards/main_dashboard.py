import streamlit as st
from streamlit_option_menu import option_menu
import milestone1_dashboard as m1
import milestone2_dashboard as m2
import milestone3_dashboard as m3
import milestone4_dashboard as m4

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="AirAware - Smart Air Quality System",
    page_icon="🌫️",
    layout="wide"
)

# -------------------------------------------------------------
# DARK THEME STYLING
# -------------------------------------------------------------
st.markdown("""
<style>
/* Main app background */
.stApp {
    background-color: #0e1117;
    color: #f5f5f5;
    font-family: 'Poppins', sans-serif;
}

/* Header */
.header {
    padding: 25px 15px;
    text-align: center;
    background: linear-gradient(90deg, #0d47a1 0%, #00acc1 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
.header h1 {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 0;
}
.header h3 {
    font-weight: 400;
    margin-top: 8px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111418;
    color: white;
    border-right: 1px solid #222;
}

/* Milestone Cards */
.card {
    background: #161a22;
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    color: #f1f1f1;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 15px #00bcd4;
}
.card h2 {
    font-size: 20px;
    color: #00e5ff;
    margin-bottom: 10px;
}
.card p {
    color: #d0d0d0;
    font-size: 14px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00bcd4, #2196f3);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 16px;
    height: 50px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    transition: 0.3s ease-in-out;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #26c6da, #42a5f5);
    transform: translateY(-2px);
}

/* Option menu labels */
div[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: transparent;
    color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# HEADER
# -------------------------------------------------------------
st.markdown("""
<div class='header'>
    <h1>🌫️ AirAware Smart Air Quality Prediction System</h1>
    <h3>Real-Time Monitoring • Forecasting • Alerts</h3>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    selected = option_menu(
        "Navigate",
        ["🏠 Home", "Milestone 1", "Milestone 2", "Milestone 3", "Milestone 4"],
        icons=['house', 'bar-chart', 'robot', 'bell', 'display'],
        default_index=0
    )

# -------------------------------------------------------------
# HOME PAGE
# -------------------------------------------------------------
if selected == "🏠 Home":
    st.markdown("### ✨ Explore AirAware Milestones")
    st.write("Each milestone represents a unique stage of the AirAware Project — from data analysis to forecasting and alert systems.")

    cols = st.columns(4)

    with cols[0]:
        st.markdown("""
        <div class='card'>
            <h2>📊 Milestone 1</h2>
            <p>Data exploration, pollutant visualization, and trend analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Milestone 1", use_container_width=True):
            selected = "Milestone 1"

    with cols[1]:
        st.markdown("""
        <div class='card'>
            <h2>🤖 Milestone 2</h2>
            <p>Model training and evaluation for pollutant forecasting.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Milestone 2", use_container_width=True):
            selected = "Milestone 2"

    with cols[2]:
        st.markdown("""
        <div class='card'>
            <h2>🚨 Milestone 3</h2>
            <p>Live alert generation and AQI prediction dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Milestone 3", use_container_width=True):
            selected = "Milestone 3"

    with cols[3]:
        st.markdown("""
        <div class='card'>
            <h2>📈 Milestone 4</h2>
            <p>Comprehensive web-based visualization and admin reports.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Milestone 4", use_container_width=True):
            selected = "Milestone 4"

# -------------------------------------------------------------
# MILESTONE SELECTIONS
# -------------------------------------------------------------
if selected == "Milestone 1":
    st.markdown("## 📊 Milestone 1: Air Quality Data Explorer")
    m1.show_dashboard()

elif selected == "Milestone 2":
    st.markdown("## 🤖 Milestone 2: Model Training & Evaluation")
    m2.show_dashboard()

elif selected == "Milestone 3":
    st.markdown("## 🚨 Milestone 3: Alerts & Trends")
    m3.show_dashboard()

elif selected == "Milestone 4":
    st.markdown("## 📈 Milestone 4: Web Dashboard & Admin")
    m4.show_dashboard()
