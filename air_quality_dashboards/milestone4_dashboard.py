import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta

def show_dashboard():
    # ------------------ Title ------------------
    st.markdown("""
    <h2 style="color:#2e7d32;">📊 Air Quality Forecast Dashboard</h2>
    <p style="color:gray; margin-top:-10px;">Milestone 4: Working Application (Weeks 7–8)</p>
    """, unsafe_allow_html=True)

    # ------------------ Load and Clean Data ------------------
    df = pd.read_csv("data/air_quality.csv")

    # Ensure correct data types
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['AQI'] = pd.to_numeric(df['AQI'], errors='coerce')

    # Scale normalized AQI (0–1) to real-world scale (0–500)
    if df['AQI'].max() <= 1:
        df['AQI'] = df['AQI'] * 500

    df = df.sort_values('Date')

    # ------------------ Sidebar ------------------
    st.sidebar.header("🧭 Forecast Controls")

    city = st.sidebar.selectbox("Monitoring Station", sorted(df['City'].unique()))
    pollutant = st.sidebar.selectbox("Pollutant", ['PM2.5', 'PM10', 'NO2', 'O3'])
    forecast_horizon = st.sidebar.selectbox("Forecast Horizon", ["24 Hours", "3 Days", "7 Days"])

    st.sidebar.markdown("---")
    st.sidebar.markdown("📆 **Data Span:**")
    st.sidebar.write(f"From {df['Date'].min().date()} to {df['Date'].max().date()}")
    st.sidebar.markdown("---")

    # ------------------ Filter Data ------------------
    df_city = df[df['City'] == city].sort_values('Date').dropna(subset=[pollutant, 'AQI'])
    last_aqi = df_city['AQI'].dropna().iloc[-1]

    # --- Determine AQI Category (CPCB standard) ---
    if last_aqi <= 50:
        aqi_bucket = "Good"
    elif last_aqi <= 100:
        aqi_bucket = "Satisfactory"
    elif last_aqi <= 200:
        aqi_bucket = "Moderate"
    elif last_aqi <= 300:
        aqi_bucket = "Poor"
    elif last_aqi <= 400:
        aqi_bucket = "Very Poor"
    else:
        aqi_bucket = "Severe"

    # ------------------ Top Row Layout ------------------
    col1, col2 = st.columns((1, 2))

    # --- Current AQI Indicator ---
    with col1:
        st.subheader("🌤️ Current Air Quality")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=last_aqi,
            title={'text': "AQI"},
            gauge={
                'axis': {'range': [0, 500]},
                'bar': {'color': "#388e3c"},
                'steps': [
                    {'range': [0, 50], 'color': "#66bb6a"},
                    {'range': [51, 100], 'color': "#d4e157"},
                    {'range': [101, 200], 'color': "#ffca28"},
                    {'range': [201, 300], 'color': "#ff7043"},
                    {'range': [301, 400], 'color': "#8d6e63"},
                    {'range': [401, 500], 'color': "#6a1b9a"}
                ]
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.write(f"**City:** {city}")
        st.write(f"**Current AQI:** {last_aqi:.2f}")
        st.write(f"**Category (CPCB Standard):** {aqi_bucket}")

    # --- ARIMA Forecast Chart ---
    with col2:
        st.subheader(f"📈 {pollutant} Forecast (ARIMA)")
        data = df_city[['Date', pollutant]].set_index('Date')
        forecast_days = {"24 Hours": 1, "3 Days": 3, "7 Days": 7}[forecast_horizon]

        try:
            model = ARIMA(data[pollutant], order=(2, 1, 2))
            model_fit = model.fit()
        except:
            model = ARIMA(data[pollutant], order=(1, 1, 1))
            model_fit = model.fit()

        forecast = model_fit.get_forecast(steps=forecast_days)
        pred = forecast.predicted_mean
        ci = forecast.conf_int()
        future_dates = pd.date_range(data.index[-1] + timedelta(days=1), periods=forecast_days)

        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=data.index, y=data[pollutant],
            mode='lines+markers', name='Historical'
        ))
        fig_forecast.add_trace(go.Scatter(
            x=future_dates, y=pred,
            mode='lines+markers', name='Forecast', line=dict(dash='dot')
        ))
        fig_forecast.add_trace(go.Scatter(
            x=future_dates, y=ci.iloc[:, 0],
            mode='lines', line_color='lightgrey', name='Lower CI'
        ))
        fig_forecast.add_trace(go.Scatter(
            x=future_dates, y=ci.iloc[:, 1],
            fill='tonexty', mode='lines', line_color='lightgrey', name='Upper CI'
        ))
        fig_forecast.update_layout(
            title=f"{pollutant} Forecast using ARIMA",
            xaxis_title="Date",
            yaxis_title=f"{pollutant} (µg/m³)"
        )
        st.plotly_chart(fig_forecast, use_container_width=True)

    st.divider()

    # ------------------ Pollutant Trends ------------------
    st.subheader("📉 Pollutant Trends (Last 7 Days)")
    pollutants_to_plot = ['PM2.5', 'NO2', 'O3']
    fig_trend = px.line(
        df_city.tail(7), x='Date', y=pollutants_to_plot,
        markers=True, title="Weekly Pollutant Trend"
    )
    fig_trend.update_layout(legend_title_text="Pollutant", yaxis_title="Concentration (µg/m³)")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # ------------------ Alert Notifications ------------------
    st.subheader("🔔 Alert Notifications")
    alert_col1, alert_col2 = st.columns(2)
    with alert_col1:
        st.success("✅ Good air quality observed\n\n📅 Today, 10:00 AM")
    with alert_col2:
        st.warning("⚠️ Moderate air quality expected\n\n📅 Tomorrow, 10:00 AM")

    st.info("📊 ARIMA model updated successfully\n\n🕓 Yesterday, 11:30 PM")
