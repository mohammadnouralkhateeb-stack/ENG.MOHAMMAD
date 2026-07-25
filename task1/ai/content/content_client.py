from decouple import config
from openai import OpenAI

class ContentClient:
    def __init__(self):
        self.client = OpenAI(api_key=config('OPENAI_API_KEY'))
        
    def generate(self, prompt):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    