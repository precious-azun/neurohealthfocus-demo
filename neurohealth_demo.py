import streamlit as st
import speech_recognition as sr
import spacy
import matplotlib.pyplot as plt

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

st.set_page_config(page_title="Stroke Assistant", layout="centered")
st.title("🧠 Stroke Recovery Assistant")
st.write("This assistant will help clinicians capture symptoms, generate SOAP notes, and visualize a recovery path.")

# --- Function to transcribe audio ---
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening for symptoms (please speak clearly)...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.write("🔄 Transcribing...")
        try:
            transcription = recognizer.recognize_google(audio)
            return transcription
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# --- Function to extract SOAP notes ---
def generate_soap_notes(text):
    doc = nlp(text)
    subjective = [ent.text for ent in doc.ents if ent.label_ == 'SYMPTOM']
    objective = [ent.text for ent in doc.ents if ent.label_ == 'EXAM_RESULT']
    assessment = [ent.text for ent in doc.ents if ent.label_ == 'DIAGNOSIS']
    plan = [ent.text for ent in doc.ents if ent.label_ == 'TREATMENT']
    return subjective, objective, assessment, plan

# --- Function to recommend recovery plan ---
def generate_recovery_plan(subjective):
    recovery_plan = ""
    if "fatigue" in subjective:
        recovery_plan += "🛌 Rest and light physical therapy. "
    if "speech difficulty" in subjective:
        recovery_plan += "🗣️ Prioritize speech therapy. "
    if "weakness" in subjective:
        recovery_plan += "🏋️ Focus on strength training in physical therapy. "
    if recovery_plan == "":
        recovery_plan = "⚠️ No specific recovery suggestion based on symptoms."
    return recovery_plan

# --- UI: Audio Transcription ---
if st.button("🎙️ Start Recording"):
    transcription = transcribe_audio()
    st.write("📝 **Transcribed Text:**", transcription)

    # Generate and display SOAP
    subj, obj, assess, plan = generate_soap_notes(transcription)

    st.subheader("🧾 SOAP Notes")
    st.write("**Subjective:**", ", ".join(subj) if subj else "Not detected")
    st.write("**Objective:**", ", ".join(obj) if obj else "Not detected")
    st.write("**Assessment:**", ", ".join(assess) if assess else "Not detected")
    st.write("**Plan:**", ", ".join(plan) if plan else "Not detected")

    # --- Recovery Plan ---
    st.subheader("🧩 Personalized Recovery Plan")
    recovery = generate_recovery_plan(subj)
    st.success(recovery)

    # --- Patient Metadata ---
    st.subheader("📥 Patient Metadata")
    age = st.number_input("Patient Age", min_value=18, max_value=100, value=65)
    onset_days = st.number_input("Days Since Stroke Onset", min_value=0, max_value=365, value=3)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    # --- Real-Time Recovery Dashboard ---
    st.subheader("📊 Recovery Dashboard")

    # Simulate a score
    recovery_score = max(0, 100 - (onset_days * 0.7 + age * 0.3))
    st.metric(label="🧠 Estimated Recovery Index", value=f"{recovery_score:.1f}")

    # Simple projected recovery chart
    days = list(range(0, 91, 10))
    recovery_curve = [min(100, recovery_score + (d * 0.5)) for d in days]

    fig, ax = plt.subplots()
    ax.plot(days, recovery_curve, marker='o', color='green')
    ax.set_title("Projected Recovery Curve (Next 90 Days)")
    ax.set_xlabel("Days Post-Onset")
    ax.set_ylabel("Estimated Recovery Index")
    ax.grid(True)
    st.pyplot(fig)

    st.info("🔒 This output is for clinical assistance only. Not a substitute for medical advice.")
