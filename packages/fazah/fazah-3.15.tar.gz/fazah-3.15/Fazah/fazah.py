from deep_translator import GoogleTranslator
from langdetect import detect

class Fazah:
    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.translator = GoogleTranslator(source='auto', target='en')

    def process_text(self, text):
        try:
            if not text.strip():
                raise ValueError("Empty input text")
            
            if len(text) > 5000:
                raise ValueError("Text length exceeds 5000 characters")
            
            # Detect the language of the input text
            source_lang = detect(text)
            
            # Translate the text to English
            english_text = self.translator.translate(text)
            
            # Feed the English text into the LLM
            llm_response = self.llm_model(english_text)
            
            # Translate the LLM response back to the original language
            translated_response = GoogleTranslator(source='en', target=source_lang).translate(llm_response)
            
            return translated_response
        
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None
        