import streamlit as st
import plotly.express as px
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client=OpenAI()
system_prompt="""You are a sustainability and energy optimization expert specializing in carbon footprint analysis.
Your task is to analyze CO₂ emissions data and provide clear, actionable insights along with realistic optimization strategies reduce carbon emissions in 50 words.
The following values are provided:
- Total CO₂ Emissions (kg): <TOTAL_CO2>
- Predicted CO₂ Emissions (kg): <PREDICTED_CO2>
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
summary_path = os.path.join(BASE_DIR, "co2_summary.json")
output_path = os.path.join(BASE_DIR, "co2_output.json")

def render(df):
    st.title("🌱 Carbon Footprint")
    data=None
    output=None
    demand=None
    try:
        with open(summary_path, "r") as f:
            data = json.load(f)
        with open(output_path, "r") as f:
            output = json.load(f)
    except:
        st.write("An error occurred")   
    total=data["total_co2_kg"]
    Predicted=output[ "co2_emissions_kg"]
    demand=output["demand"]
    st.metric("Total CO₂ Emissions (kg)", f"{total:.2f}")
    st.metric("Predicted CO2 Emissions (kg)",f"{Predicted:.2f}")
    response=client.chat.completions.create(
            
            model="gpt-4o",
            messages=[
                {
                    "role":"system","content":system_prompt
                    
                },
                {
                    "role":"user","content":f" total CO2 emisssions :{total} and Predicted CO2 emissions: {Predicted}"
                }
            ]
        )
    st.info(response.choices[0].message.content)

    