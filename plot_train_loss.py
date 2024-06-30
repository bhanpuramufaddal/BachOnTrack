from dotenv import load_dotenv
import os
from mistralai.client import MistralClient
import matplotlib.pyplot as plt

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY')
model_id = os.getenv('FINETUNED_MODEL_ID')
job_id = os.getenv('JOB_ID')

client = MistralClient(api_key=api_key)
job = client.jobs.retrieve(job_id)  
model = job.fine_tuned_model

train_steps = []
train_loss = []
valid_loss = []

for checkpoint in job.checkpoints:
    train_steps.append(checkpoint.step_number)
    train_loss.append(checkpoint.metrics.train_loss)
    valid_loss.append(checkpoint.metrics.valid_loss)

train_steps = train_steps[::-1]
train_loss = train_loss[::-1]
valid_loss = valid_loss[::-1]

plt.plot(train_steps, train_loss, label='Train Loss')
plt.plot(train_steps, valid_loss, label='Validation Loss')
plt.xlabel('Training Steps')
plt.ylabel('Loss')
plt.title('Train and Validation Loss')
plt.legend()
plt.savefig('train_loss.png')