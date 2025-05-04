import streamlit as st
import speech_recognition as sr
import spacy
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import wave

# Load spaCy model for NLP processing
nlp = spacy.load('en_core_web_sm')  # Load English model for NLP tasks

# Function to convert audio file (if needed) and transcribe to text
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio = None
    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio_data = recognizer.record(source)  # Capture the entire audio file

    try:
        transcription = recognizer.recognize_google(audio_data)
        return transcription
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio"
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition"

# Function to process the transcription and generate SOAP notes
def process_transcription_for_soap(text):
    doc = nlp(text)

    subjective = []
    objective = []
    assessment = []
    plan = []

    # Example: Extracting certain keywords or entities related to stroke recovery
    for ent in doc.ents:
        if ent.label_ == 'SYMPTOM':  # This is just an example entity
            subjective.append(ent.text)
        elif ent.label_ == 'TREATMENT':
            plan.append(ent.text)

    return subjective, objective, assessment, plan

# Function to generate a personalized recovery plan based on SOAP notes
def generate_recovery_plan(subjective):
    plan = "Based on the symptoms reported, we suggest the following recovery plan: "
    if "fatigue" in subjective:
        plan += "Rest and gradual physical therapy, including light exercises."
    if "speech difficulty" in subjective:
        plan += "Speech therapy should be prioritized."
    if "weakness" in subjective:
        plan += "Physical therapy focusing on strength building."
    return plan

# Streamlit app UI setup
st.title("Stroke Recovery Assistant")
st.write("Record a conversation between the patient and clinician to get the transcription and recovery plan.")

# Add Audio Recording functionality
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_path = "recorded_audio.wav"

    def recv(self, frame):
        with wave.open(self.audio_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(frame.sample_width)
            wf.setframerate(frame.sample_rate)
            wf.writeframes(frame.to_ndarray())
        return frame

# Streamlit session state to track recording status
if "recording" not in st.session_state:
    st.session_state.recording = False

# Function to manage start and stop recording buttons
def start_recording():
    if not st.session_state.recording:
        st.session_state.recording = True
        st.write("Recording started...")
        webrtc_streamer(key="audio", audio_processor_factory=AudioProcessor)
        st.write("Recording in progress...")

def stop_recording():
    if st.session_state.recording:
        st.session_state.recording = False
        st.write("Recording stopped.")
        # After stopping recording, transcribe the audio file
        transcription = transcribe_audio("recorded_audio.wav")
        st.write("Transcribed Text: ", transcription)

        # Process the transcription into SOAP format
        subjective, objective, assessment, plan = process_transcription_for_soap(transcription)

        # Display SOAP Notes
        st.subheader("SOAP Notes")
        st.write("**Subjective**: ", ", ".join(subjective))
        st.write("**Objective**: ", ", ".join(objective))
        st.write("**Assessment**: ", ", ".join(assessment))
        st.write("**Plan**: ", ", ".join(plan))

        # Generate a personalized recovery plan
        recovery_plan = generate_recovery_plan(subjective)
        st.write("**Personalized Recovery Plan**: ", recovery_plan)

# Handle "Start Recording" and "Stop Recording" buttons
if st.button("Start Recording"):
    start_recording()

if st.button("Stop Recording"):
    stop_recording()
