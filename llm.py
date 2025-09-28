from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

def request(dev_prompt, user_prompt):
    context = [
        { "role": "developer", "content": dev_prompt },
        { "role": "user", "content": user_prompt }
    ]
    try:
        response = client.responses.create(
            input=context,
            model=os.getenv('MODEL')
        )
        return response.output_text
    except Exception as e:
        print(f"Error occurred: {e}")
        return os.getenv('DEFAULT_RESPONSE')
