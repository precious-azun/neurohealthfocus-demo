pip install streamlit

import streamlit as st
import random

st.set_page_config(page_title="NeuroHealthFocus Triage Demo", layout="centered")
st.title("🧠 NeuroHealthFocus: Stroke Triage & Recovery")

st.markdown("""
This demo simulates how our AI platform could prioritize stroke patients and provide recovery suggestions—**without requiring real patient data**.
""")

# Input fields
st.header("1. Enter Patient Information")
age = st.slider("Age", 18, 100, 65)
severity = st.selectbox("Stroke Severity", ["Mild", "Moderate", "Severe"])
time_since_onset = st.slider("Time Since Onset (in hours)", 0, 48, 2)
symptoms = st.multiselect("Symptoms", ["Speech difficulty", "Paralysis", "Confusion", "Vision loss", "Headache"])


# Simulate triage logic
def simulate_triage(age, severity, time_since_onset, symptoms):
    urgency_map = {
        "Severe": "🚨 Urgent",
        "Moderate": "⚠️ Semi-Urgent",
        "Mild": "⏳ Routine"
    }
    if severity == "Severe" or time_since_onset < 3:
        triage = urgency_map["Severe"]
    elif severity == "Moderate" and time_since_onset < 12:
        triage = urgency_map["Moderate"]
    else:
        triage = urgency_map["Mild"]

    recovery_plan = {
        "Week 1": "Physical therapy & monitoring",
        "Week 2": "Speech therapy" if "Speech difficulty" in symptoms else "Mobility training",
        "Week 3": "Cognitive exercises",
        "Week 4": "Reassessment & goal setting"
    }
    return triage, recovery_plan


if st.button("Simulate Triage & Recovery Plan"):
    triage_result, plan = simulate_triage(age, severity, time_since_onset, symptoms)
    st.subheader("2. Triage Priority")
    st.success(f"Triage Level: {triage_result}")

    st.subheader("3. Suggested Recovery Plan")
    for week, activity in plan.items():
        st.markdown(f"**{week}:** {activity}")

    st.info("This is a simulated output. Not for clinical use.")
