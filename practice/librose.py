import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
file = 'practice/from_nature.wav'
y , sr = librosa.load(file)

A = np.abs(librosa.stft(y, hop_length=512))
DB = librosa.amplitude_to_db(A, ref=np.max)

plt.figure(figsize=(16,6))
librosa.display.specshow(DB, sr=sr, hop_length=512, 
                        x_axis='time', y_axis='log')
plt.colorbar()
plt.show()