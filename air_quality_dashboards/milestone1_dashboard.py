import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_dashboard():
    # Title
    st.markdown("""
    <h2 style="color:#2e7d32;">🌫️ Air Quality Data Explorer</h2>
    <p style="color:gray; margin-top:-10px;">Milestone 1: Working Application (Weeks 1–2)</p>
    """, unsafe_allow_html=True)

    # Load data
    df = pd.read_csv("data/air_quality.csv")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date')

    # Sidebar Controls
    st.sidebar.header("🧭 Data Controls")

    city = st.sidebar.selectbox("Location", sorted(df['City'].unique()))
    min_date, max_date = df['Date'].min(), df['Date'].max()
    date_range = st.sidebar.date_input("Time Range", [min_date, max_date])

    pollutants = [c for c in df.columns if c not in ['City', 'Date', 'AQI', 'AQI_Bucket']]
    selected_pollutants = st.sidebar.multiselect("Pollutants", pollutants, default=pollutants[:3])

    st.sidebar.markdown("### 🧹 Data Quality")
    completeness = 100 - df.isna().mean().mean() * 100
    validity = 100 * df.notna().mean().mean()
    st.sidebar.progress(int(completeness))
    st.sidebar.write(f"Completeness: **{completeness:.0f}%**")
    st.sidebar.progress(int(validity))
    st.sidebar.write(f"Validity: **{validity:.0f}%**")

    # Filtered data
    mask = (df['City'] == city) & (
        df['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
    )
    filtered_df = df.loc[mask, ['Date', 'City', 'AQI', 'AQI_Bucket'] + selected_pollutants]

    # --- Layout for Main Dashboard ---
    col1, col2 = st.columns((2, 1))

    # PM2.5 Time Series (Left)
    with col1:
        st.subheader("📈 PM2.5 Time Series")
        if 'PM2.5' in selected_pollutants:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(filtered_df['Date'], filtered_df['PM2.5'], marker='o', color='#388e3c')
            ax.set_xlabel("Date")
            ax.set_ylabel("Concentration (µg/m³)")
            ax.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)
        else:
            st.info("Select PM2.5 from the sidebar to view its time series.")

    # Pollutant Correlations (Right)
    with col2:
        st.subheader("🔗 Pollutant Correlations")
        corr = filtered_df[selected_pollutants].corr()
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(corr, annot=True, cmap="Greens", fmt=".2f", ax=ax)
        st.pyplot(fig)

    st.divider()

    # --- Statistical Summary ---
    st.subheader("📊 Statistical Summary")
    desc = filtered_df[selected_pollutants].describe().T
    st.dataframe(desc.style.background_gradient(cmap="Greens"), use_container_width=True)

    st.divider()

    # --- Distribution Analysis ---
    col3, col4 = st.columns((1, 2))
    with col3:
        st.subheader("📦 Distribution Analysis")
        selected_pollutant_dist = st.selectbox("Select Pollutant", selected_pollutants)
    with col4:
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.histplot(filtered_df[selected_pollutant_dist].dropna(), kde=True, color='#4caf50', ax=ax)
        ax.set_xlabel(f"{selected_pollutant_dist} Concentration (µg/m³)")
        st.pyplot(fig)
