import streamlit as st
import speech_recognition as sr
import spacy
import pandas as pd
import plotly.express as px
import random
import time

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Streamlit setup
st.set_page_config(page_title="NeuroHealthFocus Assistant", layout="centered")
st.title("🧠 NeuroHealthFocus: Stroke Assistant + ER Dashboard")

# --- AUDIO TRANSCRIPTION ---
st.header("🎙️ 1. Voice Symptom Capture")

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Please describe symptoms clearly.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.write("Transcribing...")
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, could not understand audio."
        except sr.RequestError:
            return "Speech recognition error."

def generate_soap_notes(text):
    doc = nlp(text)
    subjective = [ent.text for ent in doc.ents if ent.label_ == 'SYMPTOM']
    objective = [ent.text for ent in doc.ents if ent.label_ == 'EXAM_RESULT']
    assessment = [ent.text for ent in doc.ents if ent.label_ == 'DIAGNOSIS']
    plan = [ent.text for ent in doc.ents if ent.label_ == 'TREATMENT']
    return subjective, objective, assessment, plan

def generate_recovery_plan(subjective):
    plan = ""
    if "fatigue" in subjective:
        plan += "- Rest and gradual physical therapy.\n"
    if "speech difficulty" in subjective:
        plan += "- Initiate speech therapy.\n"
    if "weakness" in subjective:
        plan += "- Strength-based physical therapy.\n"
    return plan if plan else "Standard recovery and monitoring."

if st.button("🎤 Start Recording"):
    transcription = transcribe_audio()
    st.write("**Transcribed:**", transcription)

    subjective, objective, assessment, plan_items = generate_soap_notes(transcription)

    st.subheader("📄 SOAP Notes")
    st.write("**Subjective:**", ", ".join(subjective))
    st.write("**Objective:**", ", ".join(objective))
    st.write("**Assessment:**", ", ".join(assessment))
    st.write("**Plan:**", ", ".join(plan_items))

    st.subheader("🛠️ Recovery Plan")
    st.code(generate_recovery_plan(subjective))

# --- TRIAGE FORM ---
st.markdown("---")
st.header("🧾 2. Stroke Triage Form")

age = st.slider("Age", 18, 100, 65)
severity = st.selectbox("Stroke Severity", ["Mild", "Moderate", "Severe"])
onset = st.slider("Onset Time (hours ago)", 0, 48, 4)
symptoms = st.multiselect("Select Symptoms", ["Speech difficulty", "Paralysis", "Confusion", "Vision loss", "Headache"])

def get_triage(age, severity, onset, symptoms):
    if severity == "Severe" or onset <= 3:
        return "🚨 Urgent"
    elif severity == "Moderate" or onset <= 12:
        return "⚠️ Semi-Urgent"
    return "⏳ Routine"

if st.button("📊 Submit Triage"):
    result = get_triage(age, severity, onset, symptoms)
    st.success(f"Triage Level: {result}")

# --- FHIR-SIMULATED PATIENT DATA ---
st.markdown("---")
st.header("📈 3. Real-Time FHIR Dashboard")

# Auto-refresh every 10 seconds
count = st.experimental_get_query_params().get("refresh", [0])[0]
count = int(count)
st.experimental_set_query_params(refresh=str(count + 1))
time.sleep(10)
st.rerun()

# Simulated patient data (would be pulled from FHIR/EMR API in production)
def get_fhir_patient_data():
    triage_levels = ["Urgent", "Semi-Urgent", "Routine"]
    return pd.DataFrame({
        "Patient ID": [f"PT-{i:03}" for i in range(1, 21)],
        "Triage Level": random.choices(triage_levels, weights=[4, 6, 10], k=20),
        "Bed Assigned": random.choices(["Yes", "No"], weights=[15, 5], k=20)
    })

df = get_fhir_patient_data()

# Dashboard Charts
st.subheader("🌀 Triage Distribution")
fig = px.pie(df, names="Triage Level", title="Triage Case Load")
st.plotly_chart(fig)

# Bed Availability
total_beds = 25
occupied_beds = df["Bed Assigned"].value_counts().get("Yes", 0)
free_beds = total_beds - occupied_beds

st.subheader("🛏️ Bed Availability")
st.progress(free_beds / total_beds)
st.write(f"🟢 {free_beds} out of {total_beds} beds available")

if free_beds < 5:
    st.error("⚠️ ALERT: Low bed availability. Notify ER staff immediately!")

st.subheader("📋 Current Patients (FHIR-Fetched)")
st.dataframe(df)

st.markdown("---")
st.info("Prototype | Simulated FHIR API | Not for Clinical Use")
