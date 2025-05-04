import streamlit as st
import speech_recognition as sr
import spacy
import pandas as pd
import random
import time

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

st.set_page_config(page_title="Stroke Recovery Assistant", layout="wide")

# --- Function: Transcribe audio input ---
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak your symptoms clearly.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.success("✅ Audio captured! Transcribing...")
        try:
            transcription = recognizer.recognize_google(audio)
            return transcription
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Speech recognition service error."

# --- Function: Generate SOAP notes from text ---
def generate_soap_notes(text):
    doc = nlp(text)
    subjective = [ent.text for ent in doc.ents if ent.label_ in ['SYMPTOM', 'DISEASE']]
    objective = [ent.text for ent in doc.ents if ent.label_ == 'EXAM_RESULT']
    assessment = [ent.text for ent in doc.ents if ent.label_ == 'DIAGNOSIS']
    plan = [ent.text for ent in doc.ents if ent.label_ == 'TREATMENT']
    return subjective, objective, assessment, plan

# --- Function: Generate recovery plan ---
def generate_recovery_plan(subjective):
    plan = "Based on reported symptoms, consider the following plan: "
    if "fatigue" in subjective:
        plan += "🛌 Rest and light activity. "
    if "weakness" in subjective:
        plan += "🏋️‍♀️ Strength-based physical therapy. "
    if "speech" in subjective:
        plan += "🗣️ Consider speech therapy. "
    if not subjective:
        plan += "No specific recovery recommendations found."
    return plan

# --- Function: Simulated FHIR Patient Data ---
def get_patient_data():
    return {
        "Name": "John Doe",
        "Age": 68,
        "Onset": "2024-12-05",
        "Diagnosis": "Post-stroke aphasia",
        "Last Updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# --- Function: Simulated Real-Time Bedflow Dashboard ---
def bedflow_dashboard():
    st.subheader("🏥 Real-Time Bedflow Dashboard")
    st.caption("Auto-refreshes every few seconds. Alerts trigger when availability is low.")

    num_beds = 25
    available_beds = random.randint(0, num_beds)

    st.metric("Total Beds", num_beds)
    st.metric("Available Beds", available_beds)

    if available_beds < 5:
        st.error("⚠️ Alert: Low bed availability! Please prepare for high ER congestion.")
    else:
        st.success("✅ Bed availability is within safe range.")

    # Auto-refresh every 10 seconds
    time.sleep(10)
    st.rerun()

# --- UI Section ---
st.title("🧠 Stroke Recovery Assistant (Voice + Dashboard)")

# Patient Info
st.subheader("🩺 Patient Summary")
patient_info = get_patient_data()
st.json(patient_info)

# Initialize session state for storing transcription result
if "transcription" not in st.session_state:
    st.session_state.transcription = ""

# Start voice-based SOAP note generation
if st.button("🎙️ Start Recording Symptoms"):
    st.session_state.transcription = transcribe_audio()  # Store transcription in session state
    st.write("**You said:**", st.session_state.transcription)  # Display transcription

    subj, obj, assess, plan = generate_soap_notes(st.session_state.transcription)

    st.subheader("📋 SOAP Notes")
    st.write("**Subjective:**", ", ".join(subj))
    st.write("**Objective:**", ", ".join(obj))
    st.write("**Assessment:**", ", ".join(assess))
    st.write("**Plan:**", ", ".join(plan))

    recovery_plan = generate_recovery_plan(subj)
    st.subheader("📌 Recovery Recommendation")
    st.success(recovery_plan)

# Bedflow Section
if st.button("📊 View Real-Time Bedflow Dashboard"):
    bedflow_dashboard()

st.caption("Note: This is a demo. Not for clinical decision-making.")
