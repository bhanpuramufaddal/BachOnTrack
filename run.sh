#!/bin/bash

# Take an argument named num_rows
num_rows=$1
training_steps=$2

# Run the python script
python dataloaders/bach.py --num_rows $num_rows

# Check if the command throws an error, and abort if it does
if ! python get_info.py --training_steps $training_steps; then
	echo "Error: get_info.py command failed."
	exit 1
fi

python finetune.py --training_steps $training_steps
python plot_train_loss.py