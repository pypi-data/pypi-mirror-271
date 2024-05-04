from Fazah.Fazah import Fazah
import google.generativeai as genai

# Set up the Google Gemini API key
API_KEY = "AIzaSyDNTqJoy4ZSLagfj8eD9HiKgPU2h-gUsGw"
genai.configure(api_key=API_KEY)

# Create an instance of the Google Gemini model
model = genai.GenerativeModel('gemini-pro')

# Create an instance of the LLM model using Google Gemini
def create_llm_model():
    def generate(prompt):
        response = model.generate_content(prompt)
        return response.text

    return generate

# Create an instance of the Polyglot class
llm_model = create_llm_model()
polyglot = Fazah(llm_model)

# Test case 1: English to English
print("Test case 1: English to English")
english_text = "Hello, how are you?"
print("Input:", english_text)
spanish_response = polyglot.process_text(english_text)
print("Output:", spanish_response)
print()

# Test case 2: French to English
print("Test case 2: French to English")
french_text = "Bonjour, comment allez-vous?"
print("Input:", french_text)
french_response = polyglot.process_text(french_text)
print("Output:", french_response)
print()

# Test case 3: German to English
print("Test case 3: German to English")
german_text = "Guten Tag, wie geht es Ihnen?"
print("Input:", german_text)
german_response = polyglot.process_text(german_text)
print("Output:", german_response)
print()
