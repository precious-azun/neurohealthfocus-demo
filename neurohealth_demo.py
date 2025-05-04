import streamlit as st

# Set up Streamlit page
st.set_page_config(page_title="NeuroHealthFocus Stroke Triage", layout="centered")
st.title("🧠 NeuroHealthFocus: Stroke Triage & Recovery")

st.header("1. Enter Patient Information")

# Input fields for clinical data
age = st.slider("Age", 18, 100, 65)
severity = st.selectbox("Stroke Severity", ["Mild", "Moderate", "Severe"])
time_since_onset = st.slider("Time Since Onset (in hours)", 0, 48, 2)
symptoms = st.multiselect("Symptoms", ["Speech difficulty", "Paralysis", "Confusion", "Vision loss", "Headache"])

# SOAP note input fields
st.header("2. Enter SOAP Notes")
subjective = st.text_area("Subjective (Patient's Symptoms, Concerns)")
objective = st.text_area("Objective (Physical Exam Findings, Results)")
assessment = st.text_area("Assessment (Diagnosis or Evaluation)")
plan = st.text_area("Plan (Treatment, Follow-up, Recommendations)")


# Function to simulate triage and recovery plan
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


# Simulate and show results
if st.button("Simulate Triage & Recovery Plan"):
    triage_result, plan = simulate_triage(age, severity, time_since_onset, symptoms)
    st.subheader("3. Triage Priority")
    st.success(f"Triage Level: {triage_result}")
    st.subheader("4. Suggested Recovery Plan")
    for week, activity in plan.items():
        st.markdown(f"**{week}:** {activity}")

    st.subheader("5. SOAP Documentation")
    st.write("**Subjective:**", subjective)
    st.write("**Objective:**", objective)
    st.write("**Assessment:**", assessment)
    st.write("**Plan:**", plan)

    st.info("This is a simulated output. Not for clinical use.")
