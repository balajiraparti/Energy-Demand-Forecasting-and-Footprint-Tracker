import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def render(df):

    st.title("Energy Consumption Overview")

    st.markdown(
        """
        This overview presents household-level electricity consumption
        and explains how units consumed impact the electricity bill
        as per MSEDCL residential slab rates.
        """
    )

    df = pd.read_csv("data/electricity_demand.csv")

    avg_temp = df["Temperature"].mean()
    avg_humidity = df["Humidity"].mean()

    raw_avg_units = df["Demand"].mean()
    avg_monthly_demand = min(max(raw_avg_units, 80), 300)

    def calculate_msedcl_bill(units):
        fixed_charge = 120
        slab1 = min(units, 100) * 4.43
        slab2 = min(max(units - 100, 0), 200) * 9.64
        slab3 = min(max(units - 300, 0), 200) * 12.83
        slab4 = max(units - 500, 0) * 14.33
        return slab1 + slab2 + slab3 + slab4 + fixed_charge

    monthly_bill = calculate_msedcl_bill(avg_monthly_demand)
    yearly_bill = monthly_bill * 12

    st.subheader("Key Summary Metrics")

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Temperature (°C)", f"{avg_temp:.2f}")
    c2.metric("Avg Humidity (%)", f"{avg_humidity:.2f}")
    c3.metric("Avg Monthly Units (kWh)", f"{avg_monthly_demand:.0f}")

    st.markdown(
        f"""
        Estimated Monthly Bill: ₹{monthly_bill:,.2f}  
        Estimated Yearly Bill: ₹{yearly_bill:,.2f}
        """
    )


    st.subheader("Units Consumed vs Electricity Bill")

    unit_range = np.arange(50, 601, 25)
    bill_values = [calculate_msedcl_bill(u) for u in unit_range]

    fig, ax = plt.subplots()
    ax.plot(unit_range, bill_values, marker='o')
    ax.set_xlabel("Monthly Units (kWh)")
    ax.set_ylabel("Electricity Bill (₹)")
    ax.set_title("Electricity Units vs Monthly Bill")
    st.pyplot(fig)

    st.subheader("Temperature vs Monthly Electricity Consumption")

    fig, ax = plt.subplots()
    ax.scatter(
        df["Temperature"].to_numpy(),
        np.clip(df["Demand"].to_numpy(), 50, 600),
        alpha=0.6
    )
    ax.set_xlabel("Average Temperature (°C)")
    ax.set_ylabel("Monthly Units (kWh)")
    ax.set_title("Temperature Impact on Electricity Usage")
    st.pyplot(fig)

    if "month" in df.columns:
        st.subheader("Monthly Electricity Consumption Trend")

        monthly_units = df.groupby("month")["Demand"].mean()
        monthly_units = monthly_units.clip(lower=80, upper=350)

        fig, ax = plt.subplots()
        ax.bar(monthly_units.index.to_numpy(), monthly_units.values)
        ax.plot(monthly_units.index.to_numpy(), monthly_units.values, marker='o')
        ax.set_xlabel("Month")
        ax.set_ylabel("Monthly Units (kWh)")
        ax.set_title("Seasonal Consumption Pattern")
        st.pyplot(fig)

    st.subheader("Slab-wise Cost Contribution")

    slab_costs = {
        "0–100": min(avg_monthly_demand, 100) * 4.43,
        "101–300": min(max(avg_monthly_demand - 100, 0), 200) * 9.64,
        "301–500": min(max(avg_monthly_demand - 300, 0), 200) * 12.83,
        "Fixed": 120
    }

    fig, ax = plt.subplots()
    ax.bar(slab_costs.keys(), slab_costs.values())
    ax.set_ylabel("Cost (₹)")
    ax.set_title("Monthly Bill Contribution by Tariff Slab")
    st.pyplot(fig)

    st.info(
        "This analysis demonstrates how household electricity units, weather factors, "
        "and tariff slabs influence monthly electricity bills."
    )

