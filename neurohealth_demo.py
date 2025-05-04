import streamlit as st
import pandas as pd
import numpy as np
import time

# Simulated data for demonstration
# In a real system, this would be real-time data pulled from hospital systems
beds_data = {
    "ICU": {"occupied": 3, "total": 5},
    "Surgery": {"occupied": 10, "total": 15},
    "General": {"occupied": 50, "total": 100},
    "ER": {"occupied": 8, "total": 10}
}

# Function to update the dashboard every few seconds
def update_bed_data():
    while True:
        for key in beds_data:
            beds_data[key]["occupied"] = np.random.randint(0, beds_data[key]["total"] + 1)
        time.sleep(5)

# Set up Streamlit page
st.set_page_config(page_title="Hospital Bedflow Dashboard", layout="wide")
st.title("Hospital Bedflow Management Dashboard")

# Display Bed Availability
st.header("Real-Time Bed Availability")
st.write("This dashboard provides real-time data on bed occupancy in various hospital units.")

# Display beds data
bed_df = pd.DataFrame(beds_data).T
bed_df["availability"] = bed_df["total"] - bed_df["occupied"]
st.dataframe(bed_df)

# Simulate updates every 5 seconds
update_bed_data()

