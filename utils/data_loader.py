import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/electricity_demand.csv")
    df.columns = df.columns.str.lower()
    df["date"] = pd.to_datetime(df.iloc[:, 0])
    df.rename(columns={df.columns[1]: "consumption"}, inplace=True)
    return df
