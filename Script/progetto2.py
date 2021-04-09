import librosa
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Eseguire in /Users/nicola/Desktop/tesi
'''
@getcwd:    restituisce la directory di lavoro corrente
@path.join: int unisce uno o più componenti del percorso. Concatena vari componenti del percorso con esattamente un separatore di directory ('/') dopo ogni parte non vuota tranne l'ultimo componente del percorso.
'''
base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")  # base_path/apk
audio_folder = os.path.join(apk_folder, "audio")  # base_path/apk/audio

print(base_path)
print(apk_folder)
print(audio_folder)

'''
@.split():  Split a string into a list where each word is a list item:
'''
# header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
header = 'filename chroma_stft spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'

for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()

'''
@open():    "w" - Write - Opens a file for writing, creates the file if it does not exist
@with:      Dopo aver aperto il file, with crea un gestore di contesto e chiuderà automaticamente il gestore di file quando avrà finito. Mentre con open avremmo dovuto chiuderlo noi.
            Senza with avremmo dovuto usare dopo la scrittura file.close()

@Writer:    Capire Ritorna un oggetto writer per covertire un dato e per permettere di scrivere all'interno del file che abbiamo generato o aperto per scrivere una nuva riga nel file si usa il metodo 
            @writerow passando la strigna da inserire. Nel nostro caso trasformera la stringa in un csv (abbiamo creato l'oggetto writer) andando a sostituire agli spazi le virgole
'''
file = open('data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)

'''
@genres:        crea una lista di die elementi "trusted" and "malware"
@os.listdir:    restituisce una lista contenente i nomi delle voci nella directory data da path. L'elenco è in ordine arbitrario. Non include le voci speciali "." e '..' anche se sono presenti nella directory.
'''
genres = 'trusted malware'.split()
for g in genres:
    for filename in os.listdir(
            f"{audio_folder}/{g}"):  # Per ogni file all'interno della path definita sopra audio_folder/trusted ed audio_folder/malware
        if filename == ".DS_Store":  # Se il file è .DS_Store continuo a l'terazione senza eseguire le istruzioni del ciclo
            continue

        songname = f'{audio_folder}/{g}/{filename}'
        y, sr = librosa.load(songname, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        # rmse = librosa.feature.rmse(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        # to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        to_append += f' {g}'

        file = open('data.csv', 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(to_append.split())
