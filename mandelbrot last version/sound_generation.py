import wave
import numpy as np


def sound_gen(amp_x=1,amp_y=1,freq_x=53.0,freq_y=54.0):
    samplerate = 96000
    secs = 3
    time = np.linspace(0, secs, secs*samplerate)
    audio_left = amp_x * np.sin(2 * time) + amp_x * np.sin(2 * np.pi * freq_x * time)
    audio_left = (audio_left * (2 ** 15 - 1)).astype("<h")
    time = np.linspace(0, secs, secs*samplerate)
    audio_right = amp_y * np.sin(2 * time) + amp_y * np.sin(2 * np.pi * freq_y * time)
    audio_right = (audio_right * (2 ** 15 - 1)).astype("<h")
    audio = np.column_stack((audio_left, audio_right))

    # Open the wave file
    with wave.open("sound.wav", "w") as f:
      # Set the number of channels and sample width
      f.setnchannels(2) # Change to 2 for stereo
      f.setsampwidth(2)
      f.setframerate(samplerate)
      # Set the number of frames
      f.setnframes(len(audio))
      # Write the audio data to the wave file
      f.writeframes(audio.tobytes())
      f.close()

def sound_from_fractal():
    pass