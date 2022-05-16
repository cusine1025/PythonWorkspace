import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
y , sr = librosa.load('C:\\Users\\gram_\\OneDrive\\바탕 화면\\PythonWorkspace\\practice\\QueenBeePiping2017.wav') # librosa.load() : 오디오 파일을 로드한다.

D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512)) #n_fft : window size / 이 때, 음성의 길이를 얼마만큼으로 자를 것인가? 를 window라고 부른다.
DB = librosa.amplitude_to_db(D, ref=np.max) #amplitude(진폭) -> DB(데시벨)로 바꿔라

plt.figure(figsize=(16,6))
librosa.display.specshow(DB,sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.colorbar()
plt.show()