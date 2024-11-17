from deep_translator import GoogleTranslator
import logging

class TranslationService:
    def __init__(self, client):
        self.client = client

    def secure_translate_text(self, text, target_lang):
        try:
            translator = GoogleTranslator(source='auto', target=target_lang)
            return translator.translate(text)
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return None

    def secure_enhance_medical_terms(self, text):
        try:
            completion = self.client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=[{
                    "role": "system",
                    "content": "You are a medical transcription expert. Correct and enhance any medical terminology in the following text while preserving the original meaning. Don't be General, just translate what input you receive."
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.3,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Medical term enhancement error: {str(e)}")
            return text
