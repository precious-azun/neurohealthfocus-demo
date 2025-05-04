import streamlit as st
import speech_recognition as sr
import spacy

# Load spaCy model for NLP processing
nlp = spacy.load('en_core_web_sm')


# Function to transcribe audio
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for symptoms...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for input from the microphone
        st.write("Transcribing audio...")
        try:
            transcription = recognizer.recognize_google(audio)  # Using Google Speech Recognition API
            return transcription
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error with the request to the speech recognition service."


# Function to generate SOAP notes
def generate_soap_notes(text):
    doc = nlp(text)
    subjective = [ent.text for ent in doc.ents if ent.label_ == 'SYMPTOM']
    objective = [ent.text for ent in doc.ents if ent.label_ == 'EXAM_RESULT']
    assessment = [ent.text for ent in doc.ents if ent.label_ == 'DIAGNOSIS']
    plan = [ent.text for ent in doc.ents if ent.label_ == 'TREATMENT']

    return subjective, objective, assessment, plan


# Function to generate recovery plan based on symptoms
def generate_recovery_plan(subjective):
    recovery_plan = "Based on the symptoms reported, we suggest the following recovery plan: "
    if "fatigue" in subjective:
        recovery_plan += "Rest and gradual physical therapy, including light exercises. "
    if "speech difficulty" in subjective:
        recovery_plan += "Speech therapy should be prioritized. "
    if "weakness" in subjective:
        recovery_plan += "Physical therapy focusing on strength building. "
    return recovery_plan


# Streamlit app interface
st.title("Stroke Recovery Assistant")
st.write("Click 'Start Recording' to begin capturing audio symptoms.")

# Start Recording Button
if st.button('Start Recording'):
    transcription = transcribe_audio()  # Start recording and transcribing
    st.write("Transcribed Text: ", transcription)  # Show transcription

    # Generate SOAP notes based on transcription
    subjective, objective, assessment, plan = generate_soap_notes(transcription)

    # Display SOAP notes
    st.subheader("SOAP Notes")
    st.write("**Subjective:**", ", ".join(subjective))
    st.write("**Objective:**", ", ".join(objective))
    st.write("**Assessment:**", ", ".join(assessment))
    st.write("**Plan:**", ", ".join(plan))

    # Generate and display recovery plan
    recovery_plan = generate_recovery_plan(subjective)
    st.subheader("Personalized Recovery Plan")
    st.write(recovery_plan)

    st.info("This is a simulated output. Not for clinical use.")
