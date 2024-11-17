import streamlit as st
import os
from groq import Groq
import logging
import audio_recorder_streamlit as ast
from src.security import BasicSecurity
from src.audio_processor import AudioProcessor
from src.translation_service import TranslationService
from src.ui_components import UIComponents
from src.config import LANGUAGES

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
# Initialize services
security = BasicSecurity()
client = Groq(api_key=st.secrets["api_key"])
audio_processor = AudioProcessor(client)
translation_service = TranslationService(client)

# Initialize session state
if 'recording_state' not in st.session_state:
    st.session_state.recording_state = 'stopped'
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None

def main():
    UIComponents.setup_page()
    
    source_lang, target_lang = UIComponents.display_language_selectors(LANGUAGES)
    
    st.subheader("Voice Recording")
    
    start, stop, reset = UIComponents.display_recording_controls()
    
    if start:
        st.session_state.recording_state = 'recording'
        st.session_state.audio_bytes = None
        st.rerun()
    
    if stop:
        st.session_state.recording_state = 'stopped'
        st.rerun()
    
    if reset:
        st.session_state.recording_state = 'stopped'
        st.session_state.audio_bytes = None
        st.rerun()

    if st.session_state.recording_state == 'recording':
        st.markdown("""
            <div class="recording-status" style="background-color: #ff4b4b; color: white;">
                Recording in progress... 🎙️
            </div>
        """, unsafe_allow_html=True)
        
        audio_bytes = ast.audio_recorder(
            pause_threshold=60.0,
            sample_rate=44100
        )
        if audio_bytes:
            st.session_state.audio_bytes = audio_bytes
    
    if st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes, format="audio/wav")
        
        with st.spinner("Processing audio..."):
            audio_file = audio_processor.secure_save_audio(st.session_state.audio_bytes)
            
            if audio_file:
                transcription = audio_processor.secure_transcribe_audio(audio_file)
                
                if transcription:
                    encrypted_transcription = security.encrypt_text(transcription)
                    enhanced_text = security.encrypt_text(
                        translation_service.secure_enhance_medical_terms(
                            security.decrypt_text(encrypted_transcription)
                        )
                    )
                    
                    translation = security.encrypt_text(
                        translation_service.secure_translate_text(
                            security.decrypt_text(enhanced_text), 
                            LANGUAGES[target_lang]
                        )
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                            <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #ddd;">
                                <h3>Original Text</h3>
                                <p>{}</p>
                            </div>
                        """.format(security.decrypt_text(enhanced_text)), unsafe_allow_html=True)
                        
                        if st.button("🔊 Play Original"):
                            audio_file = audio_processor.secure_text_to_speech(
                                security.decrypt_text(enhanced_text),
                                LANGUAGES[source_lang]
                            )
                            if audio_file:
                                st.audio(audio_file)
                                os.remove(audio_file)
                    
                    with col2:
                        st.markdown("""
                            <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #ddd;">
                                <h3>Translation</h3>
                                <p>{}</p>
                            </div>
                        """.format(security.decrypt_text(translation)), unsafe_allow_html=True)
                        
                        if st.button("🔊 Play Translation"):
                            audio_file = audio_processor.secure_text_to_speech(
                                security.decrypt_text(translation),
                                LANGUAGES[target_lang]
                            )
                            if audio_file:
                                st.audio(audio_file)
                                os.remove(audio_file)

if __name__ == "__main__":
    main()
