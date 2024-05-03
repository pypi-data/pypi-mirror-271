from anthropic import Anthropic
from Library.myfunctions import Fazah
client = Anthropic(
    api_key="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",
    )

def create_anthropic_llm_model():
    def generate(prompt):
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system="You are a helpful assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        if isinstance(response.content, list):
            response.content = response.content[0].text
        elif hasattr(response.content, 'text'):
            response.content = response.content.text
        return response.content
    return generate

llm_model = create_anthropic_llm_model()
fazah = Fazah(llm_model)

# Test case 1: German to English (Anthropic)
print("Test case 3: Igblo to English")
german_text = "Kọwaa echiche nke chirality na kemịkalụ organic yana otu o siri metụta njirimara dị iche iche nke enantiomers, dị ka thalidomide."
german_response = fazah.process_text(german_text)
print("Output:", german_response)
print()