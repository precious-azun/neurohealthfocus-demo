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
        st.info("🎤 Listening... Doctor, please describe the patient's condition.")
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

    recovery = generate_recovery_plan(selected_symptoms)
    st.subheader("📌 Initial Therapy Recommendation")
    st.success(recovery)

    st.info("🎙️ Now the doctor can speak for deeper assessment...")

    if st.button("🎧 Start Doctor's Voice Assessment"):
        text = transcribe_audio()
        st.write("**Doctor said:**", text)

        subj, obj, assess, plan = generate_soap_notes(text)

        st.subheader("📋 SOAP Notes")
        st.write("**Subjective:**", ", ".join(subj) or "None")
        st.write("**Objective:**", ", ".join(obj) or "None")
        st.write("**Assessment:**", ", ".join(assess) or "None")
        st.write("**Plan:**", ", ".join(plan) or "None")

# Final section: Bedflow Dashboard
if st.button("📊 View Real-Time Bedflow"):
    bedflow_dashboard()

st.caption("Note: This is a prototype for demonstration purposes only.")
