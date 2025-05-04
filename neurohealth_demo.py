import streamlit as st
import speech_recognition as sr
import spacy
from pydub import AudioSegment
from io import BytesIO

# Load spaCy model for NLP processing
nlp = spacy.load('en_core_web_sm')  # Load English model for NLP tasks


# Function to convert audio file (if needed) and transcribe to text
def transcribe_audio(file):
    recognizer = sr.Recognizer()
    audio = None
    # Convert the uploaded audio to WAV format using pydub
    if file.type == "audio/mp3":
        audio = AudioSegment.from_mp3(file)
        audio = audio.set_channels(1).set_frame_rate(16000)  # Convert to mono and set a suitable frame rate
        with BytesIO() as wav_file:
            audio.export(wav_file, format="wav")
            wav_file.seek(0)
            audio_file = sr.AudioFile(wav_file)
    elif file.type == "audio/wav":
        audio_file = sr.AudioFile(file)

    # Recognize speech using Google's API
    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio_data = recognizer.record(source)  # Capture the entire audio file
    try:
        # Use Google API for transcribing the speech to text
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

    # You can expand this with more complex rules or machine learning models
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

st.write(
    "Upload an audio file of a conversation between the patient and clinician to get the transcription and recovery plan.")

# File uploader for audio
uploaded_audio = st.file_uploader("Upload a patient conversation (Audio)", type=["wav", "mp3"])

if uploaded_audio:
    st.audio(uploaded_audio, format='audio/wav')  # Play the uploaded audio
    transcription = transcribe_audio(uploaded_audio)  # Transcribe the audio
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

