import streamlit as st
import spacy
import pandas as pd
import random
import time

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

st.set_page_config(page_title="Stroke Recovery Assistant", layout="wide")

# --- Function: Generate SOAP notes from patient data ---
def generate_soap_notes(symptoms, name, age):
    # Subjective section
    subjective = f"I met with {name}, a {age}-year-old patient who came here today feeling {', '.join(symptoms)}."

    # Objective section (vital signs can be added here if needed, for now it's just a placeholder)
    objective = "Vital signs were not recorded in this demo, but typically, we would include blood pressure, heart rate, and other relevant measures."

    # Assessment section (AI-based analysis based on symptoms)
    assessment = "Based on the symptoms provided, AI suggests that the patient may be experiencing post-stroke aphasia, motor impairment, or cognitive dysfunction. Further medical examination is needed."

    # Plan section (recommendations based on symptoms)
    plan = ""

    # Assigning treatment plans based on symptoms
    if "Speech impairment" in symptoms:
        plan += "Recommend speech therapy and communication aids.\n"

    if "Paralysis" in symptoms or "Weakness" in symptoms:
        plan += "Recommend physical therapy, mobility exercises, and strength training.\n"

    if "Fatigue" in symptoms:
        plan += "Encourage rest, gradual physical activity, and cognitive rest.\n"

    if "Memory loss" in symptoms or "Cognitive issues" in symptoms:
        plan += "Recommend cognitive rehabilitation, memory exercises, and psychological support.\n"

    # Additional plan if multiple symptoms are present
    if "Speech impairment" in symptoms and "Paralysis" in symptoms:
        plan += "Consider multidisciplinary therapy, combining speech therapy and physical therapy.\n"

    if not plan:
        plan = "No specific therapy recommended based on selected symptoms."

    return subjective, objective, assessment, plan


# --- Function: Generate recovery plan based on selected symptoms ---
def generate_recovery_plan(symptoms_list):
    response = "Suggested recovery plan:\n"

    # Keywords for specific therapies
    aphasia_keywords = ['speech', 'talk', 'language', 'unable to speak', 'speech impairment']
    paralysis_keywords = ['paralysis', 'weakness', 'unable to move', 'muscle weakness']
    fatigue_keywords = ['fatigue', 'tired', 'low energy']
    cognitive_keywords = ['memory loss', 'difficulty concentrating', 'cognitive issues']

    # Check for aphasia (speech impairment)
    if any(word in symptoms_list for word in aphasia_keywords):
        response += "🧠 Possible post-stroke aphasia detected. Recommend speech therapy.\n"

    # Check for paralysis/weakness
    if any(word in symptoms_list for word in paralysis_keywords):
        response += "💪 Paralysis/weakness detected. Recommend physical therapy, mobility exercises, and strength training.\n"

    # Check for fatigue
    if any(word in symptoms_list for word in fatigue_keywords):
        response += "🛌 Fatigue detected. Recommend rest, low activity, and gradual exercise.\n"

    # Check for cognitive issues
    if any(word in symptoms_list for word in cognitive_keywords):
        response += "🧠 Cognitive issues detected. Recommend cognitive exercises and memory training.\n"

    # Additional consideration for combining symptoms
    if "speech" in symptoms_list and "paralysis" in symptoms_list:
        response += "💪🧠 Combining paralysis and speech impairment. Consider multidisciplinary therapy, including speech and physical therapy.\n"

    # If no recommendations found, ensure a general message
    if response.strip() == "Suggested recovery plan:":
        response += "No specific therapy found based on selected symptoms."

    return response


# --- Function: Real-Time Bedflow Dashboard ---
def bedflow_dashboard():
    st.subheader("🏥 Real-Time Bedflow Dashboard")
    st.caption("Auto-refreshes every few seconds. Alerts trigger when availability is low.")

    num_beds = 25
    available_beds = random.randint(0, num_beds)

    st.metric("Total Beds", num_beds)
    st.metric("Available Beds", available_beds)

    if available_beds < 5:
        st.error("⚠️ Alert: Low bed availability!")
    else:
        st.success("✅ Bed availability is safe.")

    time.sleep(10)
    st.rerun()


# --- Main UI ---
st.title("🧠 Stroke Recovery Assistant")

# Step 1: Enter patient info
with st.form("patient_form"):
    st.subheader("👤 Patient Entry")
    name = st.text_input("Patient Name", value="Subject 1")
    age = st.number_input("Age", min_value=1, max_value=120, value=68)
    stroke_date = st.date_input("Date of Stroke")

    # Step 2: Select symptoms from dropdown
    symptoms = [
        "Paralysis", "Speech impairment", "Fatigue", "Memory loss", "Weakness", "Cognitive issues", "Other"
    ]
    selected_symptoms = st.multiselect("Select Symptoms", symptoms)

    submitted = st.form_submit_button("🔍 Analyze Symptoms")

if submitted:
    st.subheader("🩺 Patient Summary")
    st.json({
        "Name": name,
        "Age": age,
        "Date of Stroke": str(stroke_date),
        "Symptoms": selected_symptoms,
        "Last Updated": time.strftime("%Y-%m-%d %H:%M:%S")
    })

    # Generate SOAP notes and recovery plan
    subj, obj, assess, plan = generate_soap_notes(selected_symptoms, name, age)
    st.subheader("📋 SOAP Notes")
    st.write("**Subjective:**", subj)
    st.write("**Objective:**", obj)
    st.write("**Assessment:**", assess)
    st.write("**Plan:**", plan)

    st.subheader("📌 Initial Therapy Recommendation")
    st.success(generate_recovery_plan(selected_symptoms))

# Final section: Bedflow Dashboard
if st.button("📊 View Real-Time Bedflow"):
    bedflow_dashboard()

st.caption("Note: This is a prototype for demonstration purposes only.")
