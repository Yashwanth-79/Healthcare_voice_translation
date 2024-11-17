import os
import tempfile
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
import logging
from groq import Groq

class AudioProcessor:
    def __init__(self, client):
        self.client = client

    def secure_save_audio(self, audio_bytes):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb') as f:
                os.chmod(f.name, 0o600)
                f.write(audio_bytes)
                return f.name
        except Exception as e:
            logging.error(f"Error saving audio: {str(e)}")
            return None

    def secure_transcribe_audio(self, audio_file):
        try:
            with open(audio_file, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_file, file.read()),
                    model="whisper-large-v3",
                    response_format="verbose_json"
                )
                return transcription.text
        except Exception as e:
            logging.error(f"Transcription error: {str(e)}")
            return None
        finally:
            try:
                os.remove(audio_file)
            except:
                pass

    def secure_text_to_speech(self, text, lang_code):
        try:
            tts = gTTS(text=text, lang=lang_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', mode='wb') as f:
                os.chmod(f.name, 0o600)
                tts.save(f.name)
                return f.name
        except Exception as e:
            logging.error(f"Text-to-speech error: {str(e)}")
            return None