import os
from mistralai.client import MistralClient
from dotenv import load_dotenv
from argparse import ArgumentParser
import time

load_dotenv()
api_key = os.environ.get('MISTRAL_API_KEY')

client = MistralClient(api_key=api_key)

def check_completed_job(_id):

    job = client.jobs.retrieve(_id)
    while job.status == 'RUNNING' or job.status == 'QUEUED':
        job = client.jobs.retrieve(_id)
        job_status = job.status
        print(f"Job {job.id} is queued")
        time.sleep(100)

    print(f"Job {job.id} is {job.status}")
    print(f"Fine-tuned model endpoint: {job.fine_tuned_model}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--job_id", type=str, required=True)
    args = parser.parse_args()

    check_completed_job(args.job_id)