import os
from mistralai.client import MistralClient
from mistralai.models.jobs import TrainingParameters
from dotenv import load_dotenv, set_key 
from argparse import ArgumentParser
import time

TRAINING_STEPS = 1000

# load_dotenv("mistral-music/.env")
load_dotenv()
MODEL_ID = "open-mistral-7b"
api_key = os.environ.get('MISTRAL_API_KEY')
client = MistralClient(api_key=api_key)

from check_job_status import check_completed_job  

def run(train_file, validation_file, training_steps):

    with open(train_file, "rb") as f:
        training_data = client.files.create(file=("train.jsonl", f))

    with open(validation_file, "rb") as f:
        validation_data = client.files.create(file=("validation.jsonl", f))

    ft_job = client.jobs.create(
        model="open-mistral-7b",
        training_files=[training_data.id],
        validation_files=[validation_data.id],
        dry_run=False,
        hyperparameters=TrainingParameters(
            training_steps=training_steps,
            learning_rate=0.0001,
            )
    )

    print(f"Job {ft_job.id} is running")
    check_completed_job(ft_job.id)
    ft_job = client.jobs.retrieve(ft_job.id)
    ft_model = ft_job.fine_tuned_model

    set_key(dotenv_path='.env', key_to_set="FINETUNED_MODEL_ID", value_to_set=ft_model)
    set_key(dotenv_path='.env', key_to_set="JOB_ID", value_to_set=ft_job.id)

    print(f"Fine-tuned model endpoint: {ft_model}")

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="datasets/bach")
    parser.add_argument("--training_steps", type=int, default=TRAINING_STEPS)
    args = parser.parse_args()

    train_file = os.path.join(args.dataset_dir, "train.jsonl")
    validation_file = os.path.join(args.dataset_dir, "validation.jsonl")

    run(train_file, validation_file, training_steps=args.training_steps)

    