import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib
model = joblib.load("electricity_prediction_model.pkl")
import co2_prediction as co
footprint=0
def render(df):
    st.title(" Demand Forecast")

    hour = st.sidebar.slider("Hour", 0, 23, 18)
    dayofweek = st.sidebar.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 4)
    month = st.sidebar.slider("Month", 1, 12, 7)
    dayofyear = st.sidebar.slider("Day of Year", 1, 366, 210)

    year = st.sidebar.selectbox(
    "Year (Forecast Year)",
    options=list(range(2026, 2030)) )

    weekofyear = st.sidebar.slider("Week of Year", 1, 53, 30)
    quarter = st.sidebar.slider("Quarter", 1, 4, 3)
    is_weekend = st.sidebar.selectbox("Is Weekend (0=No, 1=Yes)",options=[0,1])
    temperature = st.sidebar.slider("Temperature (°C)", -5.0, 50.0, 35.0)
    humidity = st.sidebar.slider("Humidity (%)", 0, 100, 70)
    demand_lag_24hr = st.sidebar.slider("Demand Lag (24 Hours)", 0, 10000, 4200)
    demand_lag_168hr = st.sidebar.slider("Demand Lag (168 Hours)", 0, 10000, 4100)
    rolling_mean_24hr = st.sidebar.slider("Rolling Mean (24 Hours)", 0, 10000, 4150)
    rolling_std_24hr = st.sidebar.slider("Rolling Std (24 Hours)", 0, 5000, 250)

    df=pd.DataFrame([{
        "hour": hour,
        "dayofweek": dayofweek,
        "month": month,
        "year": year,
        "dayofyear": dayofyear,
        "weekofyear": weekofyear,
        "quarter": quarter,
        "is_weekend": is_weekend,
        "Temperature": temperature,
        "Humidity": humidity,
        "Demand_lag_24hr": demand_lag_24hr,
        "demand_lag_168hr": demand_lag_168hr,
        "demand_rolling_mean_24hr": rolling_mean_24hr,
        "demand_rolling_std_24hr": rolling_std_24hr
    }])
    if st.button("Predict Demand"):
        prediction = model.predict(df)[0]

        st.success(f"Predicted Electricity Demand: {prediction:.2f}")

        with st.expander("Model Input"):
            st.dataframe(df)
        footprint=co.get_co2_footprint(prediction)
        st.success(f"Predicted CO2 footprint:{footprint:}")
        
        
