## Generating ABC sequence inspired by the style of Bach.

We trained a Mistral 7b model to generate music in ABC format int he style of Bach.
We have trained the model on 2 kinds of tasks:

1. Generate an ABC composition given a starting sequence of ABC notes with a single coice.
2. Gnenerate an ABC comosition with multiple voices given an ABC sequence.

We have created interface in Gradio to interact with our model.

### Datasets
We have used [MusicPile](https://huggingface.co/datasets/m-a-p/MusicPile) dataset as a source and processed it to create our own SFT Dataset. The code for processing the dataset can be found [here](BachOnTrack/dataloaders/bach.py).

### How to Run the code

```sh
sh run.sh {number of samples used in finetuning} {training steps}
```

The entire dataset contain 4,00,000 samples but do not use more than 1,50,000 samples.

### Installation

```sh
pip install -r requirements.txt

# use brew to install abcmidi and fluidsmith for mac.
# In case of Linux, use apt-get
brew install abcmidi
brew install fluidsynth
```

### Launch Gradio

#### For Autocomplete Task

```
python autocomplete_gradio.py
```

#### For generating multi-voice music given abc sequence

```
python add_instuments_gradio.py
```

#### Generate Song

This script combines above 2 tasks, it uses autocompletion followed by adding multiple instuments.

```
python make_song_gradio.py
```

### Presentation
#### [Video](https://drive.google.com/file/d/1X8h3CqkjCTflOl46gcovunlC1YoY4J_A/view?usp=drive_link)
#### [Google Slides](https://docs.google.com/presentation/d/11IcnbdRHho4NRhtQzwq22lT9n8xiBSqabtFkFf6LIgQ/edit?usp=drive_link)
