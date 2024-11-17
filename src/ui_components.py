import streamlit as st
import audio_recorder_streamlit as ast
import os

class UIComponents:
    @staticmethod
    def setup_page():
        st.set_page_config(page_title="NaoMedical", layout="wide")
        st.markdown(" ## Healthcare Translation Web App with Generative AI")
        st.text("By [Nao Medical](https://naomedical.com)")

    @staticmethod
    def display_language_selectors(languages):
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox("Source Language", list(languages.keys()), index=0)
        with col2:
            target_lang = st.selectbox("Target Language", list(languages.keys()), index=1)
        return source_lang, target_lang

    @staticmethod
    def display_recording_controls():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            start = st.button("🎙️ Start Recording", 
                        type="primary" if st.session_state.recording_state != 'recording' else "secondary",
                        disabled=st.session_state.recording_state == 'recording')
        
        with col2:
            stop = st.button("⏹️ Stop", 
                        type="primary" if st.session_state.recording_state == 'recording' else "secondary",
                        disabled=st.session_state.recording_state != 'recording')
        
        with col3:
            reset = st.button("🔄 Reset",
                        disabled=st.session_state.recording_state == 'recording')
        
        return start, stop, reset