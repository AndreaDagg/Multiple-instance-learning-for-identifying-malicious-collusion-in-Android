import librosa
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

'''
------------------------------------ CONSIGLI SU COME RUNNARE IL CODICE -----------------------------
Lo script genera due file data.csv data.arff a partire dagli audio splittati andando a valutare se il file è un acid e 
quindi andando a leggere il tipo di classe (trusted,broadcast_intent,shared_preferences,external_storage)

Inserire di volta in volta un blocco di cartelle splitted nella cartella Acid_Splitted o Trusted_Splitted
Modificare la variagile @genres con il nome cartella che si sta elaborando (file trusted / oppure acid)
In pannello di contorllo in risparmi energetico abbasssare la potenza della cpu 
Copiare di volta in volta i file .csvg e .arff in una nuova cartella "Running" generati ed eliminarli per generare i nuovi
In questo modo si evitano alte temperature prolungate ed il tempo d'esecuzione è accettabile
'''

# Eseguire in /Users/nicola/Desktop/tesi
'''
@getcwd:    restituisce la directory di lavoro corrente
@path.join: int unisce uno o più componenti del percorso. Concatena vari componenti del percorso con esattamente un separatore di directory ('/') dopo ogni parte non vuota tranne l'ultimo componente del percorso.
'''
base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")  # base_path/apk
audio_folder = os.path.join(apk_folder, "audio")  # base_path/apk/audio
trusted_Acid_Folder = os.path.join(apk_folder, "trusted_Acid")
trusted_Apk_Folder = os.path.join(audio_folder, "trusted_audio_trusted_apk")

print("basePath: ", base_path)
print("Apk Folder: ", apk_folder)
print("Audio Folder: ", audio_folder)

'''
@header: E' la stringa della prima riga del file csv
@.split():  Split a string into a list where each word is a list item:

'''
# header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
header = 'filename chroma_stft spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'

for i in range(1, 21):
    header += f' mfcc{i}'
header += ' class'
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
Genera il file .arff automaticamente andando a prendere i nomi dei file
ATTENZIONE: Le classi sono statiche
'''
fileArff = open('data.arff', 'a', newline='')
fileArff.write("@relation virus\n\n")
fileArff.write("@attribute virus_bag{")

for wav in os.listdir(trusted_Acid_Folder):
    fileArff.write(f'{str(wav.split(".")[0])}{".wav"}{","}')
for wav in os.listdir(trusted_Apk_Folder):
    fileArff.write(f'{str(wav)}{","}')
fileArff.write("}\n")
fileArff.write("@attribute bag relational\n")

for label in header:
    if (label == "class" or label == "filename"):  # salto le label class e label
        continue
    fileArff.write(f'{"@attribute"} {label} {"real"}\n')
fileArff.write("@end bag\n")
fileArff.write("@attribute class{trusted,broadcast_intent,shared_preferences,external_storage}\n\n")
fileArff.write("@data\n")
fileArff.close()
'''
@genres:        crea una lista di elementi "trusted" and "malware"
@os.listdir:    restituisce una lista contenente i nomi delle voci nella directory data da path. L'elenco è in ordine arbitrario. Non include le voci speciali "." e '..' anche se sono presenti nella directory.
'''
splitted_Folder = os.path.join(audio_folder, "Splitted_Wav")
# path al set originale non al file audio
acidDatasetFolder = os.path.join(base_path, "Dataset_Acid\\Dataset_Acid\\archive")
print("\nAcidFolder: ", acidDatasetFolder)

# Blocco per eseguire tutto in un solo run dello script - Attenzioen indentazione
'''
genres = 'Acid_Splitted/Trusted_Splitted'.split("/")
for trustedOrAcidDirectory in genres:
'''

'''
Blocco per eseguire lo script in più running - evitare alte temperature prolungate
@genres la variabile che prende il nome della cartella che si sta analizzando (Trusted or Acid)
Decommentare la corrispondente dell'elaborazione per far funzionare lo script correttamente
'''
# genres = "Trusted_Splitted"
genres = "Acid_Splitted"

i = 1
trustedOrAcidDirectory = genres
for filename_SplittedFolder in os.listdir(f"{splitted_Folder}\\{trustedOrAcidDirectory}"):
    print("Iterata:  ", i)
    i += 1
    # Per ogni file all'interno della path definita sopra audio_folder/trusted ed audio_folder/malware
    if filename_SplittedFolder == ".DS_Store":  # Se il file è .DS_Store continuo a l'iterazione senza eseguire le istruzioni del ciclo
        continue
    else:
        classe = "trusted"
        pathSplittedAudioDirectory = f'{splitted_Folder}\\{trustedOrAcidDirectory}\\{filename_SplittedFolder}'  # path del file audio i-mo
        # Titolo corrisponde al nome della cartella i-ma senza .wav
        audioTitle = filename_SplittedFolder.split(".wav")[0]
        print("\nLog-> File: ", audioTitle)

        if (trustedOrAcidDirectory == "Acid_Splitted"):
            # songTitle = songname.split("\\")[6].split(".")[0]  # Titolo senza Path ed Estensione del file

            # cerca il tipo di malware
            for setFold in os.listdir(acidDatasetFolder):
                if setFold == ".DS_Store":
                    continue
                else:
                    apkInt = 0
                    # sappiamo che ogni set ha 2 apk quidni iteriamo direttamente su due senza andare a leggere il contenuto della directory
                    while (apkInt < 2):
                        apkFolder = os.path.join(acidDatasetFolder, f'{setFold}\\{"apk"}')
                        apk = os.listdir(apkFolder)

                        if (audioTitle == str(apk[apkInt].split(".")[0])):
                            # path alla stringa dal leggere
                            with open(f'{acidDatasetFolder}\\{setFold}\\{"description.txt"}', 'r') as reader:
                                # estrggo dalla stringa il tipo di malware
                                malwareType = reader.read().split(":")[1]
                                #print("Malware Type: ", malwareType)
                                classe = malwareType
                        apkInt += 1
        to_append_arff = ""
        iterationNumb = 1
        for splittedAudio in os.listdir(pathSplittedAudioDirectory):
            # path completa al file da analizzare
            splittedAudioPath = os.path.join(pathSplittedAudioDirectory, f'{splittedAudio}')

            '''
            @librosa.load:  loading dei primo 30sec del file audio convertendo il segnale in mono
                            Ritorna:    Y   -> la serie temporale dell'audio. Un segnale audio, indicato con y , e rappresentato come un unidimensionale numpy.ndarray di valori in virgola mobile. y [t] corrisponde all'ampiezza della forma d'onda al campione t ."
                                        SR  -> frequenza di campionamento di Y
                            https://medium.com/comet-ml/applyingmachinelearningtoaudioanalysis-utm-source-kdnuggets11-19-e160b069e88
            @croma_stft:    Calcola un cromagramma da una forma d'onda o uno spettrogramma di potenza.
            @spectral_centroid:     Calcola il centroide spettrale
            @spectral_bandwidth:    Calcola la larghezza di banda spettrale del p-esimo ordine.
            @spectral_rolloff:      Compute roll-off frequency.
            @mfcc:                  Mel-frequency cepstral coefficients (MFCCs)
            ---------------------------------------------------------------------
            @np.mean:       Restituisce la media degli elementi dell'array.
            
            '''

            y, sr = librosa.load(splittedAudioPath, mono=True, duration=30)
            chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
            # rmse = librosa.feature.rmse(y=y)
            spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            to_append = f'{audioTitle}{".wav"} {np.mean(chroma_stft)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
            # if     è il primo elemento della bag devo precedere alla virgolette il nome id della bag
            # else   devo iniziare con \n per differenziare le istanze delle bag e non va più audio_title ma direttamente le features
            if (iterationNumb == 1):
                #print("\nPrimo")
                iterationNumb += 1
                to_append_arff = f'{audioTitle}{".wav"}{","}\"{np.mean(chroma_stft)}{","}{np.mean(spec_cent)}{","}{np.mean(spec_bw)}{","}{np.mean(rolloff)}{","}{np.mean(zcr)}{","}'
            else:
                #print("\nelse Log")
                to_append_arff += f'\\n{np.mean(chroma_stft)}{","}{np.mean(spec_cent)}{","}{np.mean(spec_bw)}{","}{np.mean(rolloff)}{","}{np.mean(zcr)}{","}'

            iterIndex = 1
            for e in mfcc:
                if (iterIndex == len(mfcc)):  # all'ultima features dell'istnza non mi serve inserire la virgola
                    to_append_arff += f'{np.mean(e)}'  # media dei valori in mfcc
                else:
                    to_append_arff += f'{np.mean(e)}{","}'  # media dei valori in mfcc
                to_append += f' {np.mean(e)}'  # media dei valori in mfcc
                iterIndex += 1

                # Attributo label
            to_append += f' {classe}'  # ultima colonna label
            # to_append_arff += f'{classe}\n'  # ultima colonna label

            file = open('data.csv', 'a', newline='')  # apre il file in modalità aggiunta
            writer = csv.writer(file)  # aggiungiamo la riga al file
            writer.writerow(to_append.split())

        iterationNumb = 0
        to_append_arff += f'\"{","}{classe}\n'  # ultima colonna label
        # scrivo la riga .arff
        fileArff = open('data.arff', 'a', newline='')
        fileArff.writelines(to_append_arff)
        fileArff.close()