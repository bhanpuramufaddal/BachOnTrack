from generate_music import auto_complete
import gradio as gr
import uuid
from abc2wav import abc2wav
from abc_tools import key_mapping
from random import choice

key_list = list(key_mapping.values())
pitch_list = ['treble', 'bass']

def generate_wav(abc_str, key, pitch):

  out_abc = auto_complete(abc_str, key, pitch) 
  abc_file = f"output_files/temp_{uuid.uuid4()}.abc"
  with open(abc_file, "w") as f:
      f.write(out_abc)

  wav_file = f"output_files/temp_{uuid.uuid4()}.wav"
  abc2wav(abc_file, wav_file)

  return wav_file

if __name__ == "__main__":
    
    # Set up the Gradio interface using components
    iface = gr.Interface(
        fn=generate_wav,  # Function to execute
        inputs=[gr.Textbox(lines=1, placeholder='Enter valid abc sequence', label="ABC Sequence"),
                gr.Dropdown(key_list, label="Key"),
                gr.Dropdown(pitch_list, label="Pitch")],  # Text input
        outputs="audio",  # Output audio  
    )
  
    # Launch the interface
    iface.launch()

