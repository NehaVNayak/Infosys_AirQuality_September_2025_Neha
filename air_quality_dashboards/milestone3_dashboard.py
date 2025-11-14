import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from prophet import Prophet

# -------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------
AQI_COLOR = {
    'Good': '#2ECC71',
    'Satisfactory': '#27AE60',
    'Moderate': '#F1C40F',
    'Poor': '#E67E22',
    'Very Poor': '#C0392B',
    'Severe': '#6C3483'
}

CATEGORY_COLORS = {
    'Good': '#ABEBC6',
    'Satisfactory': '#D5F5E3',
    'Moderate': '#F9E79F',
    'Poor': '#F5B7B1',
    'Very Poor': '#D98880',
    'Severe': '#BB8FCE'
}

WHO_LIMITS = {'PM2.5': 15, 'PM10': 45, 'O3': 100}

# -------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------
@st.cache_data
@st.cache_data
def load_data(path="data/air_quality.csv"):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date')

    # convert numeric columns safely
    for col in df.columns:
        if col not in ['City', 'Date', 'AQI_Bucket']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # scale normalized AQI (0–1) → (0–500)
    if df['AQI'].max() <= 1:
        df['AQI'] = df['AQI'] * 500

    # ✅ scale pollutants (0–1) → (0–1000 µg/m³)
    pollutant_cols = ['PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO', 'NH3']
    for col in pollutant_cols:
        if col in df.columns and df[col].max() < 10:
            df[col] = df[col] * 1000

    return df

# -------------------------------------------------------------
# FORECAST FUNCTION (AQI)
# -------------------------------------------------------------
def forecast_aqi_prophet(series, periods=7):
    df = series.reset_index().rename(columns={'Date': 'ds', 'AQI': 'y'})
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=periods)
    fcst = m.predict(future).set_index('ds')
    return fcst[['yhat', 'yhat_lower', 'yhat_upper']].iloc[-periods:]

# -------------------------------------------------------------
# AQI CATEGORY FUNCTION
# -------------------------------------------------------------
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

# -------------------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------------------
def show_dashboard():
    

    st.markdown("""
    <style>
        .main-title {font-size: 36px; font-weight: 700; color: #D35400;}
        .subtitle {font-size: 20px; color: #CA6F1E; margin-bottom: 20px;}
        .forecast-card {
            padding: 15px; border-radius: 12px;
            text-align: center; font-weight: 600;
            margin: 4px; color: #333;
        }
        .alert-box {
            border-radius: 10px; padding: 12px 16px;
            margin: 6px 0; font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>Air Quality Alert System</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Milestone 3: Working Application (Weeks 5–6)</div>", unsafe_allow_html=True)

    df = load_data()

    # ------------------ Sidebar / Inputs ------------------
    col1, col2 = st.columns([2, 1])
    with col1:
        city = st.selectbox("📍 Select Location/Station", sorted(df['City'].unique()))
    with col2:
        recent_days = st.slider("Recent days to show", 7, 90, 30)

    df_city = df[df['City'] == city].set_index('Date').sort_index()
    if df_city.empty:
        st.warning("No data available for this city.")
        return

    latest = df_city.iloc[-1]
    aqi_val = float(latest.get('AQI', np.nan))
    aqi_val = 0 if np.isnan(aqi_val) else aqi_val
    aqi_cat = get_aqi_category(aqi_val)

    # ---------------------------------------------------------
    # ROW 1 – Current AQI + 7-Day AQI Forecast
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 2])

    # --- Current AQI Donut ---
    with col1:
        st.markdown("### 🌤️ Current Air Quality")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=aqi_val,
            number={'font': {'size': 36}},
            title={'text': f"{city}<br><b>{aqi_cat}</b>", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 500]},
                'bar': {'color': AQI_COLOR.get(aqi_cat, '#95A5A6')},
                'steps': [
                    {'range': [0, 50], 'color': CATEGORY_COLORS['Good']},
                    {'range': [51, 100], 'color': CATEGORY_COLORS['Satisfactory']},
                    {'range': [101, 200], 'color': CATEGORY_COLORS['Moderate']},
                    {'range': [201, 300], 'color': CATEGORY_COLORS['Poor']},
                    {'range': [301, 400], 'color': CATEGORY_COLORS['Very Poor']},
                    {'range': [401, 500], 'color': CATEGORY_COLORS['Severe']}
                ]
            }
        ))
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

    # --- AQI Forecast ---
    with col2:
        st.markdown("### 🔮 7-Day AQI Forecast")
        try:
            fcst = forecast_aqi_prophet(df_city[['AQI']], periods=7)
            fcst['category'] = fcst['yhat'].apply(get_aqi_category)
            cols = st.columns(7)
            for i, d in enumerate(fcst.index.date):
                cat = fcst['category'].iloc[i]
                color = CATEGORY_COLORS.get(cat, '#D6DBDF')
                val = int(fcst['yhat'].iloc[i])
                cols[i].markdown(
                    f"<div class='forecast-card' style='background-color:{color}'>"
                    f"<div>{d.strftime('%a')}</div>"
                    f"<div style='font-size:22px'>{val}</div>"
                    f"<div style='font-size:14px'>{cat}</div>"
                    f"</div>", unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Forecast failed: {e}")

    # ---------------------------------------------------------
    # ROW 2 – Pollutant Concentrations + Alerts
    # ---------------------------------------------------------
    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    # --- Pollutant Line Chart ---
    with col1:
        st.markdown("### 📉 Pollutant Concentrations")
        pollutants = ['PM2.5', 'PM10', 'O3']
        recent = df_city[pollutants].dropna().tail(recent_days)
        if not recent.empty:
            fig2 = go.Figure()
            for p in pollutants:
                if p in recent.columns:
                    fig2.add_trace(go.Scatter(
                        x=recent.index, y=recent[p],
                        mode='lines+markers', name=p
                    ))
                    if p in WHO_LIMITS:
                        fig2.add_trace(go.Scatter(
                            x=[recent.index.min(), recent.index.max()],
                            y=[WHO_LIMITS[p], WHO_LIMITS[p]],
                            mode='lines', name=f'{p} WHO Limit',
                            line=dict(dash='dash', color='red')
                        ))
            fig2.update_layout(
                height=420,
                yaxis_title="Concentration (µg/m³)",
                xaxis_title="Date"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No pollutant data for recent days.")

    # --- Alerts Panel ---
    with col2:
        st.markdown("### ⚠️ Active Alerts")
        alerts = []

        # AQI level alerts
        if aqi_val > 400:
            alerts.append("🚨 **Severe AQI** – Serious health impact for all groups.")
        elif aqi_val > 300:
            alerts.append("☠️ **Very Poor Air** – Respiratory illness on prolonged exposure.")
        elif aqi_val > 200:
            alerts.append("⚠️ **Poor Air Quality** – Breathing discomfort likely.")
        elif aqi_val > 100:
            alerts.append("😷 **Moderate AQI** – Sensitive groups should reduce outdoor activity.")

        # Forecast alerts (if any day >300)
        try:
            severe_days = fcst[fcst['yhat'] > 300].index.date
            if len(severe_days):
                alerts.append(f"🚨 Severe AQI expected on {', '.join(map(str, severe_days))}.")
        except Exception:
            pass

        # Pollutant WHO limit alerts
        for p, lim in WHO_LIMITS.items():
            val = df_city.iloc[-1].get(p, np.nan)
            if pd.notna(val) and val > lim:
                alerts.append(f"⚠️ {p}: {val:.1f} µg/m³ exceeds WHO limit ({lim}).")

        # Display alerts
        if alerts:
            for a in alerts:
                st.markdown(
                    f"<div class='alert-box' style='background-color:#FADBD8'>{a}</div>",
                    unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='alert-box' style='background-color:#D4EFDF'>✅ No active alerts.</div>",
                unsafe_allow_html=True)

# -------------------------------------------------------------
# RUN
# -------------------------------------------------------------
if __name__ == "__main__":
    show_dashboard()
