import os
from mistralai.client import MistralClient
from mistralai.models.jobs import TrainingParameters
from dotenv import load_dotenv
from argparse import ArgumentParser

TRAINING_STEPS = 181

# load_dotenv("mistral-music/.env")
load_dotenv()
MODEL_ID = "open-mistral-7b"
api_key = os.environ.get('MISTRAL_API_KEY')
client = MistralClient(api_key=api_key)

def get_cost(num_tokens):
    ft_cost_per_million = 0.75
    storage_cost = 2
    ft_cost_per_token = ft_cost_per_million / 1e6
    cost = storage_cost + num_tokens * ft_cost_per_token   
    return cost
    
def dry_run(train_file, validation_file, training_steps):

    with open('datasets/bach/train.jsonl', "rb") as f:
        training_data = client.files.create(file=("train.jsonl", f))

    with open('datasets/bach/validation.jsonl', "rb") as f:
        validation_data = client.files.create(file=("validation.jsonl", f))

    job_details = client.jobs.create(
        model="open-mistral-7b",
        training_files=[training_data.id],
        validation_files=[validation_data.id],
        dry_run=True,
        hyperparameters=TrainingParameters(
            training_steps=training_steps,
            learning_rate=0.0001,
            )
    )

    print(f"Job {job_details} is running")

    training_steps = job_details.training_steps
    expected_duration = job_details.expected_duration_seconds/60
    number_of_epochs = job_details.epochs
    num_tokens = job_details.train_tokens_per_step * training_steps
    ft_cost = get_cost(num_tokens)

    info = f"""
Training Steps: {training_steps}
Expected Duration: {expected_duration} minutes
Number of Epochs: {number_of_epochs}
Total Cost: {ft_cost}
"""

    print(info.strip())

    for file_obj in client.files.list().data:
        client.files.delete(file_obj.id)

def get_details(dataset_dir, training_steps):
    train_file = os.path.join(dataset_dir, "train.jsonl")
    validation_file = os.path.join(dataset_dir, "validation.jsonl")

    with open(train_file, "r") as f:
        train_data = f.read()

    with open(validation_file, "r") as f:
        validation_data = f.read()

    dry_run(train_file, validation_file, training_steps)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="datasets/bach")
    parser.add_argument("--training_steps", type=int, default=TRAINING_STEPS)
    args = parser.parse_args()

    get_details(args.dataset_dir, args.training_steps)