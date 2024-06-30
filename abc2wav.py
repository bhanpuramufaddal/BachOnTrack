from midi2audio import FluidSynth
import os

def abc2wav(abc_file, wav_file):
    
    abcfile_prefix = abc_file.split(".")[0]
    os.system(f"abc2midi {abc_file}")
    midi_file = abcfile_prefix + "1.mid"
    sound_font = "soundfonts/GeneralMontage.sf2"
    
    # Initialize FluidSynth with the custom SoundFont
    fs = FluidSynth(sound_font = sound_font)

    # Convert the MIDI file to WAV
    fs.midi_to_audio(midi_file, wav_file)

    # Remove the ABC file
    os.remove(abc_file)
    # Remove the MIDI file
    os.remove(midi_file)

    return wav_file

    # fs.play_midi(midi_file)
