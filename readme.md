## Generating ABC Sequences in the Style of Bach

We have trained a Mistral 7b model to generate music in ABC notation inspired by the style of Bach. Our model has been fine-tuned for two specific tasks:

1. Generating an ABC composition given a starting sequence of ABC notes with a single voice/instrument.
2. Generating an ABC composition with multiple voices given an initial ABC sequence.

We have created an interface in Gradio to interact with our model.

### Datasets
We used the [MusicPile](https://huggingface.co/datasets/m-a-p/MusicPile) dataset as a source and processed it to create our own supervised fine-tuning (SFT) dataset. The code for processing the dataset can be found [here](dataloaders/bach.py).

### Running the Code

To run the code, use the following command:

```sh
sh run.sh {number of samples used in finetuning} {training steps}
```

Note: The entire dataset contains 400,000 samples, but it is recommended not to use more than 150,000 samples.

### Installation

First, install the required Python packages:

```sh
pip install -r requirements.txt
```

Then, install `abcmidi` and `fluidsynth`:

For macOS:

```sh
brew install abcmidi
brew install fluidsynth
```

For Linux:

```sh
apt-get install abcmidi
apt-get install fluidsynth
```

### Launching Gradio

#### For the Autocomplete Task

To run the autocomplete task, use:

```sh
python autocomplete_gradio.py
```

#### For Generating Multi-Voice Music

To generate multi-voice music given an ABC sequence, use:

```sh
python add_instruments_gradio.py
```

#### Generate Song

This script combines the above two tasks, using autocompletion followed by adding multiple instruments:

```sh
python make_song_gradio.py
```

### Presentation
- [Video](https://drive.google.com/file/d/1X8h3CqkjCTflOl46gcovunlC1YoY4J_A/view?usp=drive_link)
- [Google Slides](https://docs.google.com/presentation/d/11IcnbdRHho4NRhtQzwq22lT9n8xiBSqabtFkFf6LIgQ/edit?usp=drive_link)
