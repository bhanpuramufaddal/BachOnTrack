import re
from dataclasses import dataclass

@dataclass
class MusicPiece:
    voice: str
    abc_sequence: str
    key: str
    pitch: str
    parent_composition: str

def get_full_key_name(key: str) -> str:
    """
    Converts a shorthand key notation to its full name.

    Parameters:
    key (str): The shorthand key notation.

    Returns:
    str: The full name of the key.
    """
    key_mapping = {
        'C': 'C Major',
        'C#': 'C# Major',
        'Cb': 'C♭ Major',
        'Cm': 'C Minor',
        'C#m': 'C# Minor',
        'Cbm': 'C♭ Minor',
        'D': 'D Major',
        'D#': 'D# Major',
        'Db': 'D♭ Major',
        'Dm': 'D Minor',
        'D#m': 'D# Minor',
        'Dbm': 'D♭ Minor',
        'E': 'E Major',
        'E#': 'E# Major',
        'Eb': 'E♭ Major',
        'Em': 'E Minor',
        'E#m': 'E# Minor',
        'Ebm': 'E♭ Minor',
        'F': 'F Major',
        'F#': 'F# Major',
        'Fb': 'F♭ Major',
        'Fm': 'F Minor',
        'F#m': 'F# Minor',
        'Fbm': 'F♭ Minor',
        'G': 'G Major',
        'G#': 'G# Major',
        'Gb': 'G♭ Major',
        'Gm': 'G Minor',
        'G#m': 'G# Minor',
        'Gbm': 'G♭ Minor',
        'A': 'A Major',
        'A#': 'A# Major',
        'Ab': 'A♭ Major',
        'Am': 'A Minor',
        'A#m': 'A# Minor',
        'Abm': 'A♭ Minor',
        'B': 'B Major',
        'B#': 'B# Major',
        'Bb': 'B♭ Major',
        'Bm': 'B Minor',
        'B#m': 'B# Minor',
        'Bbm': 'B♭ Minor'
    }

    return key_mapping.get(key, "Unknown Key")

def get_key_from_abc(abc_notation: str) -> str:
    """
    Extracts the key of a piece from its ABC notation.

    Parameters:
    abc_notation (str): A string containing the ABC notation.

    Returns:
    str: The full name of the key of the piece.
    """
    # Regular expression to find the key in the ABC notation
    key_pattern = re.compile(r'K:([A-G][#b]?m?)')

    # Search for the key in the notation
    match = key_pattern.search(abc_notation)

    # Return the full key name if found, otherwise return None
    if match:
        key_shorthand = match.group(1)
        return get_full_key_name(key_shorthand)
    else:
        return None

def get_pitch_from_voice(abc_notation: str) -> str:
    """
    Extracts the pitch (clef) from a single-voice ABC notation.

    Parameters:
    abc_notation (str): A string containing the ABC notation.

    Returns:
    str: The pitch of the voice (e.g., 'treble', 'bass').
    """
    # Regular expression to find the voice definition
    voice_pattern = re.compile(r'V:\d+\s+(treble|bass|alto|tenor|soprano)')

    # Search for the voice in the notation
    match = voice_pattern.search(abc_notation)

    # Return the pitch if found, otherwise return None
    if match:
        return match.group(1)
    else:
        return None

def get_first_line_of_abc_sequence(abc_notation: str) -> str:
    lines = abc_notation.split('\n')
    return lines[0]

def get_last_line_of_abc_sequence(abc_notation: str) -> str:
    lines = abc_notation.split('\n')
    return lines[-1]

def get_voice_list(note):
    key = get_key_from_abc(note)

    v_tags = re.findall(r'V:[0-9]', note)
    num_tags = len(set(v_tags))

    splits = re.split(r'V:[0-9]+', note)
    splits = [s.strip() for s in splits]
    prefix = splits[0]

    voices = []
    for i in range(1, num_tags + 1):

        actual_note = splits[i + num_tags]

        voice = prefix + '\n' + f"V:{i}" + '\n' + splits[i] + '\n' + f"V:{i}" + '\n' + actual_note
        voice = re.sub(r'score 1(?: \d)*', 'score 1', voice)
        voice = re.sub(r'V:[0-9]', 'V:1', voice)

        pitch = get_pitch_from_voice(voice)

        music_peice = MusicPiece(
            voice = voice,
            abc_sequence = actual_note,
            key = key,
            pitch = pitch,
            parent_composition = note)
        voices.append(music_peice)

    return voices

def add_notes(reference_note, addn_note):
    addn_voice = addn_note.abc_sequence
    combined_voice = reference_note.abc_sequence + '\n' + addn_voice
    combined_abc = reference_note.abc_sequence + '\n' + addn_voice
    combined_note = MusicPiece(
        voice = combined_voice,
        abc_sequence = combined_abc,
        key = reference_note.key,
        pitch = reference_note.pitch,
        parent_composition = None
    )
    return combined_note
