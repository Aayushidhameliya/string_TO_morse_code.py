from pydub import AudioSegment
from pydub.generators import Sine
import pygame
import os

ffmpeg_path = r"C:\path\to\your\ffmpeg\bin\ffmpeg.exe"


os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

# Morse code dictionary
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.',
    ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}


# Function to convert text to Morse code
def text_to_morse(text):
    morse_code = []
    for char in text.upper():
        if char in morse_code_dict:
            morse_code.append(morse_code_dict[char])
        else:
            morse_code.append('')  # Treat unknown characters as empty
    return ' '.join(morse_code)


# Function to generate Morse code audio
def generate_morse_audio(morse_code):
    pygame.init()
    pygame.mixer.init()

    # Set parameters for the beep sound
    frequency = 600  # Frequency in Hz
    duration_dot = 100  # Duration of a dot in milliseconds (0.1 seconds)
    duration_dash = duration_dot * 3  # Duration of a dash (3 times dot duration)
    silence = 50  # Duration of silence between dots and dashes in milliseconds (0.05 seconds)
    unit_time = duration_dot / 1000.0  # Convert dot duration to seconds

    audio = []
    for symbol in morse_code:
        if symbol == '.':
            audio.append(Sine(frequency).to_audio_segment(duration=duration_dot))
        elif symbol == '-':
            audio.append(Sine(frequency).to_audio_segment(duration=duration_dash))
        elif symbol == ' ':
            audio.append(AudioSegment.silent(duration=silence))
        else:
            continue  # Skip unknown characters

        # Add silence between symbols
        audio.append(AudioSegment.silent(duration=int(unit_time * 1000)))  # Convert seconds to milliseconds

    # Combine all audio segments
    morse_audio = sum(audio)

    # Export to .mp3 file using FFmpeg
    output_path = "morse_code.mp3"
    morse_audio.export(output_path, format="mp3", codec="libmp3lame")

    pygame.quit()


# Example usage
if __name__ == "__main__":
    text = input("enter a string:")
    morse_code = text_to_morse(text)
    print(f"Text: {text}")
    print(f"Morse Code: {morse_code}")

    generate_morse_audio(morse_code)
    print("Generated morse_code.mp3")
