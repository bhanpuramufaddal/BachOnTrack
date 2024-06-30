import os,sys
sys.path.append(os.getcwd())

from datasets import load_dataset
import pandas as pd
import re
from abc_tools import get_first_line_of_abc_sequence, get_last_line_of_abc_sequence, get_voice_list
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split
import json

from reformat_jsonl import reformat_jsonl

DATASET_NAME = 'm-a-p/MusicPile-sft'
NUM_ROWS = 65_000
VAL_SPLIT = 0.01

def remove_tags(text):
    if text.startswith("Human: "):
        text = text[7:]
    if text.startswith("Assistant: "):
        text = text[11:]

    text = text.replace("</s>", "")
    text = text.strip()
    return text

def preprocess_df(df):

    # Only keep samples from deepchoir
    df = df[df["src"] == "https://github.com/sander-wood/deepchoir"]

    df.loc[:,"instruction"] = df["instruction"].apply(remove_tags)
    df.loc[:,"output"] = df["output"].apply(remove_tags)
    df.loc[:,"input"] = df["input"].apply(remove_tags)

    # We are only looking for samples that generate ABC notation in the output
    # ABC Notation begins with 'X:'
    df = df[df["output"].str.startswith("X:")]

    df["input"] = df["input"].fillna("")
    df = df.dropna()

    # strip all the input and output values to remove trailing spaces
    df.loc[:,"input"] = df["input"].str.strip()
    df.loc[:,"instruction"] = df["instruction"].str.strip()
    df.loc[:,"output"] = df["output"].str.strip()

    # Remove empty strings
    df = df[df["instruction"] != ""]
    df = df[df["output"] != ""]

    df.reset_index(drop=True, inplace=True)
    return df

def postprocess_df(df):

    # We are only looking for samples that generate ABC notation in the output
    # ABC Notation begins with 'X:'
    df = df[df["output"].str.startswith("X:")]
    df = df.dropna()

    # strip all the input and output values to remove trailing spaces
    df.loc[:,"input"] = df["input"].str.strip()
    df.loc[:,"instruction"] = df["instruction"].str.strip()
    df.loc[:,"output"] = df["output"].str.strip()

    # Remove empty strings
    df = df[df["instruction"] != ""]
    df = df[df["input"] != ""]
    df = df[df["output"] != ""]
    return df

def create_dataframe():
    ds = load_dataset(DATASET_NAME)
    musicpile_df = pd.DataFrame(list(pd.DataFrame(ds)["train"]))
    bach_df = preprocess_df(musicpile_df)

    instruction_list = []
    input_list = []
    output_list = []

    for example in bach_df.itertuples(index=False):
        voices = get_voice_list(example.output)

        num_voices = len(voices)

        for voice in voices:

            instruction = f"Generate an ABC composition in the style of Bach with {num_voices} voices based on the given ABC sequence in the input."
            instruction_list.append(instruction)
            input_list.append(voice.abc_sequence)
            output_list.append(voice.parent_composition)

            first_line = get_first_line_of_abc_sequence(voice.abc_sequence)
            instruction = "Generate an ABC composition in the style of Bach with "
            if voice.key:
                instruction += f"Key: {voice.key},"
            if voice.pitch:
                instruction += f"pitch: {voice.pitch} voice"
            instruction += f". The piece must begin with the following input ABC sequence."

            instruction_list.append(instruction)
            input_list.append(first_line)
            output_list.append(voice.voice)

            last_line = get_last_line_of_abc_sequence(voice.abc_sequence)
            instruction = "Generate an ABC composition in the style of Bach with "
            if voice.key:
                instruction = instruction + f"Key: {voice.key},"
            if voice.pitch:
                instruction = instruction + f"pitch: {voice.pitch} voice"
            instruction += f". The piece must end with the following ABC sequence."

            instruction_list.append(instruction)
            input_list.append(last_line)
            output_list.append(voice.voice)

    all_data = pd.DataFrame({
        "instruction": instruction_list,
        "input": input_list,
        "output": output_list
    })

    return all_data

def convert_to_jsonl(dataset, filename):
    with open(filename, "w") as outfile:
        for example in dataset.itertuples(index=False):
            jsonl_example = {
                "messages": [
                    {"role": "system", "content": example.instruction},
                    {"role": "user", "content": example.input},
                    {"role": "assistant", "content": example.output}
                ]
            }
            outfile.write(json.dumps(jsonl_example) + "\n")

    reformat_jsonl(filename)

def create_dataset(dest_dir, num_rows):
    all_data = create_dataframe()

    # Shuffle the dataset
    all_data = all_data.sample(frac=1, random_state=42)
    
    train_data = all_data.iloc[:num_rows, :]
    test_data = all_data.iloc[num_rows:num_rows + 100, :]

    train_data = postprocess_df(train_data)
    test_data = postprocess_df(test_data)  

    # validation file size should be lesser than 1 mb
    trainset, validationset = train_test_split(train_data, test_size=VAL_SPLIT, random_state=42)

    train_file = os.path.join(dest_dir, "train.jsonl")
    validation_file = os.path.join(dest_dir, "validation.jsonl")
    test_file = os.path.join(dest_dir, "test.parquet")

    convert_to_jsonl(trainset, train_file)
    convert_to_jsonl(validationset, validation_file)
    test_data.to_parquet(test_file, index=False)

    print("Trainset size:", len(trainset))
    print("Validationset size:", len(validationset))
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dest_dir", type=str, default="datasets/bach")
    parser.add_argument("--num_rows", type=int, default=NUM_ROWS)
    args = parser.parse_args()
    create_dataset(args.dest_dir, num_rows=args.num_rows)







