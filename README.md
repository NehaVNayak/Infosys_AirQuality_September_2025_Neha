

---

## 📘 Overview

AirAware helps users understand:

- Historical pollution patterns  
- Dominant pollutants for each region  
- AQI categories (Good, Moderate, Poor, etc.)  
- Forecasted AQI for upcoming days  
- Trend shifts and seasonal variations  

The dashboard consists of **4 Milestone Dashboards**:

1. Data Cleaning & Visualization  
2. AQI Computation & Category Insights  
3. Prophet-based Forecasting (Dashboard 1 & 2)  
4. ARIMA Forecast + Alerts (Dashboard 3 & 4)

---

## 📂 Project Structure

```
AirAware/
│
├── main_dashboard.py
├── milestone1_dashboard.py
├── milestone2_dashboard.py
├── milestone3_dashboard.py
├── milestone4_dashboard.py
├── data/
│   └── air_quality.csv
├── requirements.txt
└── README.md
```


## 🛠️ Features

### 🔸 **Dashboard 1 – Data Exploration**
- Clean dataset, handle missing values  
- Time series visualization of pollutants  
- Correlation heatmaps  

### 🔸 **Dashboard 2 – AQI Calculation & Category Visualization**
- Compute AQI using pollutant sub-indices  
- Map AQI values to categories  
- Compare AQI across cities  

### 🔸 **Dashboard 3 – AQI Forecasting (Prophet)**
- Predict AQI for next 30 days  
- Trend + seasonal decomposition  
- Interactive city selection  

### 🔸 **Dashboard 4 – AQI Forecasting (ARIMA) + Alerts**
- ARIMA-based predictions  
- Automatic alerts if AQI rises above thresholds  
- Improved stability for short-term forecasts  

---

## 📊 Tech Stack

| Purpose | Tools |
|--------|-------|
| Language | Python |
| Framework | Streamlit |
| ML Models | Prophet, ARIMA |
| Visualization | Plotly, Seaborn, Matplotlib |
| Data Handling | Pandas, NumPy |
| Deployment | Streamlit Cloud |

---
## ⚙️ Installation

### Clone the repository
```bash
git clone https://github.com/your-username/AirAware.git
cd AirAware
```
### Install dependencies
```bash
pip install -r requirements.txt
Run the Streamlit app
```

```bash
streamlit run main_dashboard.py
```

## 📁 Dataset

The project uses city-wise daily air quality data with features like:

- PM2.5  
- PM10  
- NO₂  
- SO₂  
- CO  
- O₃  
- AQI  
- Date & Time  

## 🔮 Forecasting Models Used

### ✔️ Prophet Model  
Used for:
- Long-term AQI forecasting  
- Seasonal trend detection  
- Handling missing values and irregular intervals  

### ✔️ ARIMA Model  
Used for:
- Short-term AQI forecasting  
- Validating Prophet results  
- Improving forecast stability  

---

## 🎨 UI / Dashboard Features
- Streamlit Option Menu for clean navigation  
- Multi-page dashboard system  
- Responsive charts with Plotly  
- Alerts for unhealthy air quality  

---

## 🚀 Deployment

The app is hosted on **Streamlit Community Cloud**.

To deploy your own version:

1. Push your project to GitHub  
2. Visit: https://share.streamlit.io  
3. Select your repository  
4. Set entry file as `main_dashboard.py`  
5. Deploy 🚀  

---

## 📸 Screenshots

(Add images in an `/images` folder and update paths below)

```md
![Dashboard 1](images/screenshot1.png)
![Dashboard 2](images/screenshot2.png)
![Dashboard 3](images/screenshot3.png)
![Dashboard 4](images/screenshot4.png)
![Dashboard 5](images/screenshot5.png)
![Dashboard 6](images/screenshot6.png)
![Dashboard 7](images/screenshot7.png)
![Dashboard 8](images/screenshot8.png)
```

## 🧠 Future Enhancements
- Real-time AQI API integration  
- Mobile-friendly version  
- Geo-mapping of cities (Folium / Mapbox)  
- LSTM / Deep learning models  
- User login + personalized alerts  

---

## 📚 References
- WHO Air Quality Guidelines  
- CPCB Dataset  
- Streamlit Documentation  
- Prophet Official Docs  
- Statsmodels ARIMA Docs  

---

## 👩‍💻 Author
**Neha Nayak**  
*Air Quality Prediction & Visualization Internship Project – 2025*

