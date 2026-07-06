import google.generativeai as genai

from config import GEMINI_API_KEY, MODEL_NAME


class LLMClient:

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate(self, prompt, temperature=0.2):
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature
                }
            )

            return response.text.strip()

        except Exception as e:
            print(f"LLM Error: {e}")
            return "Unable to generate response."