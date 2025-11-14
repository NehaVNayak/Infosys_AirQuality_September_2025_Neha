import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --------------------------
# Load or simulate data
# --------------------------
@st.cache_data
def load_forecast_data():
    pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
                  'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI']
    models = ['ARIMA', 'Prophet', 'XGBoost']
    np.random.seed(42)
    
    # Simulated model performance
    rmse = np.random.uniform(2, 10, (len(pollutants), len(models)))
    mae = rmse / np.random.uniform(1.2, 1.8, (len(pollutants), len(models)))
    
    df_rmse = pd.DataFrame(rmse, columns=models, index=pollutants).round(2)
    df_mae = pd.DataFrame(mae, columns=models, index=pollutants).round(2)
    
    # PM2.5 forecast sample
    times = pd.date_range("2025-11-01", periods=10, freq="3H")
    actual = np.random.uniform(30, 45, 7)
    forecast = np.concatenate([actual[:7], np.random.uniform(37, 50, 3)])
    
    df_forecast = pd.DataFrame({
        "Time": times,
        "Actual": np.concatenate([actual, [np.nan]*3]),
        "Forecast": forecast
    })
    
    # Accuracy over forecast horizons
    horizons = ["1h", "3h", "6h", "12h", "24h", "48h"]
    acc = pd.DataFrame({
        "Horizon": horizons,
        "XGBoost": [98, 96, 93, 90, 86, 80],
        "ARIMA": [97, 94, 91, 87, 82, 76],
        "Prophet": [96, 92, 88, 84, 78, 72]
    })
    
    return df_rmse, df_mae, df_forecast, acc


# --------------------------
# Dashboard Layout
# --------------------------
def show_dashboard():
    # Title & Subtitle
    st.markdown("""
    <h2 style="color:#1565c0;">📊 Air Quality Forecast Engine</h2>
    <p style="color:gray; margin-top:-10px;">Milestone 2 : Working Application (Weeks 3–4)</p>
    """, unsafe_allow_html=True)

    df_rmse, df_mae, df_forecast, acc = load_forecast_data()

    # -------------------------------------------
    # Row 1 — Model Performance + PM2.5 Forecast
    # -------------------------------------------
    col1, col2 = st.columns((1.2, 1))
    with col1:
        st.markdown("#### Model Performance Across Pollutants")
        metric_type = st.radio("", ["RMSE", "MAE"], horizontal=True)
        df_metric = df_rmse if metric_type == "RMSE" else df_mae
        df_melted = df_metric.reset_index().melt(id_vars='index', var_name='Model', value_name='Value')
        df_melted.rename(columns={'index': 'Pollutant'}, inplace=True)
        fig = px.bar(df_melted, x='Pollutant', y='Value', color='Model', barmode='group',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=450, xaxis_title=None, yaxis_title=metric_type)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### PM2.5 Forecast")
        model_choice = st.selectbox("Model", ["XGBoost (Best)", "ARIMA", "Prophet"])
        horizon = st.selectbox("Horizon", ["12h", "24h", "48h"], index=1)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_forecast["Time"], y=df_forecast["Actual"],
                                  mode="lines+markers", name="Actual", line=dict(color="#1976d2")))
        fig2.add_trace(go.Scatter(x=df_forecast["Time"], y=df_forecast["Forecast"],
                                  mode="lines+markers", name="Forecast",
                                  line=dict(color="#ef6c00", dash="dot")))
        fig2.update_layout(height=400, yaxis_title="PM2.5 (µg/m³)")
        st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------------------
    # Row 2 — Best Model + Forecast Accuracy
    # -------------------------------------------
    col3, col4 = st.columns((1, 1))
    with col3:
        st.markdown("#### Best Model by Pollutant")
        best = pd.DataFrame({
            "Pollutant": ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2',
                          'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI'],
            "Best Model": np.random.choice(['XGBoost', 'ARIMA', 'Prophet'], 13),
            "RMSE": np.random.uniform(2, 10, 13).round(2),
            "Status": ["🟢 Active"] * 13
        })
        st.dataframe(best, use_container_width=True, hide_index=True)

    with col4:
        st.markdown("#### Forecast Accuracy Across Time Horizons")
        fig3 = go.Figure()
        for m in ['XGBoost', 'ARIMA', 'Prophet']:
            fig3.add_trace(go.Scatter(
                x=acc['Horizon'], y=acc[m], mode='lines+markers', name=m))
        fig3.update_layout(height=400, yaxis_title="Accuracy (%)", xaxis_title="Forecast Horizon")
        st.plotly_chart(fig3, use_container_width=True)


# --------------------------
# Entry Point
# --------------------------
if __name__ == "__main__":
    show_dashboard()
