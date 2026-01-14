import streamlit as st
from utils.data_loader import load_data

from views import (
   
    overview,
    forecast,
    co2_dashboard,

)

st.set_page_config(
    page_title="Green Energy Optimizer",
    layout="wide"
)

df = load_data()

if "page" not in st.session_state:
    st.session_state.page = "Overview"

c1, c2, c3, c4 = st.columns(4)


if c1.button("📊 Overview"):
    st.session_state.page = "Overview"

if c2.button("📈 Forecast"):
    st.session_state.page = "Forecast"

if c3.button("🌱 CO₂"):
    st.session_state.page = "CO2"


st.markdown("---")



if st.session_state.page == "Overview":
    overview.render(df)

elif st.session_state.page == "Forecast":
    forecast.render(df)
    
elif st.session_state.page == "CO2":
    co2_dashboard.render(df)

