from openai import AzureOpenAI
from config import AZURE_OPENAI_KEY, AZURE_API_VERSION, AZURE_OPENAI_ENDPOINT

class AzureOpenAIService:
    def __init__(self, model, temperature):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        self.model = model
        self.temperature = temperature

    def create_completion(self, prompt, system_message):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            temperature=self.temperature
        )
        return response.choices[0].message.content