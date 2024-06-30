from dotenv import load_dotenv
import os
import re
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY')
model_id = os.getenv('FINETUNED_MODEL_ID')

client = MistralClient(api_key=api_key)

def generate_music(instruction: str, input: str) -> str:
    if input:
      messages = [
        ChatMessage(role="system", content=instruction),
        ChatMessage(role="user", content=input),
      ]
    else:
      messages = [
        ChatMessage(role="system", content=instruction),
      ]

    chat_response = client.chat(
        model=model_id,
        messages= messages,
        temperature=0.5,
    )

    output_text = chat_response.choices[0].message.content
    output_text = re.sub("V:(\d+)\s+treble", "V:\\1 treble", output_text)
    output_text = re.sub("V:(\d+)\s+bass", "V:\\1 bass", output_text)
    return output_text

def auto_complete(abc_str, key,pitch):
    instruction = f"Generate an ABC composition in the style of Bach with Key: {key},pitch: {pitch} voice. The piece must begin with the following input ABC sequence."
    output_text = generate_music(instruction, abc_str)
    return output_text

def add_instuments(abc_str):
  instruction = "Generate an ABC composition in the style of Bach with 4 voices based on the given ABC sequence in the input."
  output_text = generate_music(instruction, abc_str)
  return output_text

    

  