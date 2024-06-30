from generate_music import add_instuments
import gradio as gr
import uuid
from abc2wav import abc2wav

def generate_wav(abc_str):
  out_abc = add_instuments(abc_str)  

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
      inputs=gr.Textbox(lines=1, placeholder='Enter valid abc sequence'),  # Text input
      outputs="audio",  # Output audio
  )

  # Launch the interface
  iface.launch()
