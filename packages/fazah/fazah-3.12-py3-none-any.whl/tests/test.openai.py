from Fazah import Fazah
from openai import OpenAI

OPENAI_API_KEY = "sk-proj-ggVu1RBhLnYRKdOkYeZNT3BlbkFJTeyJzT4So7GBNBqgIpAU"
client = OpenAI(api_key=OPENAI_API_KEY)




# Create an instance of the OpenAI Chat model
def create_chatgpt_llm_model():
    def generate(prompt):
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ])
        return response.choices[0].message.content

    return generate

# Create an instance of the Polyglot class
llm_model = create_chatgpt_llm_model()
fazah = Fazah(llm_model)

# Test case 1: French to English (OpenAI)
print("Test case 2: French to English")
french_text = "Bonjour, comment allez-vous?"
print("Input:", french_text)
french_response = fazah.process_text(french_text)
print("Output:", french_response)
print()

# Test case 2: German to English 
print("Test case 3: German to English")
german_text = "Guten Tag, wie geht es Ihnen?"
print("Input:", german_text)
german_response = fazah.process_text(german_text)
print("Output:", german_response)
print()
