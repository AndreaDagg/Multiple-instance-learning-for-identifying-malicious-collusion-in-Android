'''
Script per contollare se ci sono .wav in apk > trusted e non ci sono i ripettivi file .apk in script trusted
Utile per eliminare gli apk che vengono rilevati e cancellati da  windows defender
'''

import os
import zipfile
import sys
import wave
import struct

base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")
trusted_apk = os.path.join(apk_folder, "trusted")
malware_apk = os.path.join(apk_folder, "malware")
audio_folder = os.path.join(apk_folder, "audio")
trusted_audio = os.path.join(audio_folder, "trusted")
malware_audio = os.path.join(audio_folder, "malware")
trusted_Acid_Folder = os.path.join(apk_folder, "trusted_Acid")
trusted_Apk_Folder = os.path.join(audio_folder, "trusted_audio_trusted_apk")
test_Apk_Folder = os.path.join(apk_folder, "Test_Apk")

'''
createNewDirectory 
La funzione prende in input una path ed un a stringa e crea una nuova cartella 
    @return La funzione ritorna la path della cartella creata 
Se già creata precedentemente restiruisce la path
'''


def createNewDirectory(path=os.getcwd(), nameNewDirectory=""):
    pathNewDirectory = path + "\\" + nameNewDirectory
    if not os.path.exists(pathNewDirectory):
        try:
            os.mkdir(pathNewDirectory)
            print("LOG-> Directory created successfully")
            return pathNewDirectory
        except OSError as error:
            print("LOG-> Directory can not be created")
    else:
        return pathNewDirectory


'''
 @header: E' la stringa della prima riga del file csv
 @.split():  Split a string into a list where each word is a list item:

 '''


def getHeaderAttributes():
    # header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    header = 'filename chroma_stft spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'

    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' class'
    header = header.split()

    return header


'''
Funzione che ritorna una lista di tutti gli apk èpresenti delle tre  directory di file splittati

itera sulle cartelle con gli apk e poi cambia l'estensione perché i file audio potrebbere non essere stati elaborati
'''


def getDatasetWavName():
    name_list = []
    for wav in os.listdir(trusted_Acid_Folder):
        name_list.append(f'{str(wav.split(".")[0])}{".wav"}{","}')
    for wav in os.listdir(test_Apk_Folder):
        name_list.append(f'{str(wav.split(".")[0])}{".wav"}{","}')
    for wav in os.listdir(trusted_Apk_Folder):
        name_list.append(f'{str(wav)}{","}')
    return name_list


def createArff(nameFile, relation, attributes_list, attributes_type, class_list, create_result_dir=True):
    if create_result_dir:
        createNewDirectory("results")
        print("Ho creato la  cartella results...")

    print("Creo il file...")
    fileArff = open("results\\" + nameFile + ".arff", 'w', newline='')
    fileArff.write("@relation " + relation + "\n\n")  # relazione del file
    fileArff.write("@attribute virus_bag{")  # settiamo la lista di attributi bag_id or virus_id
    for wav in getDatasetWavName():
        fileArff.write(f'{str(wav)}')
    fileArff.write("}\n")

    fileArff.write("@attribute bag relational\n")  # settiamo il tipo di classe
    for label in attributes_list:
        if (label == "class" or label == "filename"):  # salto le label class e label
            continue
        fileArff.write(f'{"@attribute"} {label} {attributes_type}\n')
    fileArff.write("@end bag\n")

    # settiamo le classi
    fileArff.write("@attribute class{")
    for classElement in class_list:
        if classElement == class_list[-1]:  # contorllo per non inserire la virgola all'ultima classe
            fileArff.write(f'{classElement}')
        else:
            fileArff.write(f'{classElement}{","}')
    fileArff.write("}\n\n")
    fileArff.write("@data\n")
    fileArff.close()
    print("File ", nameFile, ".arff creato\n")


# contorlla i file erronemate eliminati
'''
apk_folder_files = list()
for wav in os.listdir(trusted_audio):

    Continue = False
    if ((wav.endswith(".wav"))):
        for apk in os.listdir(trusted_apk):

            apk_name = os.path.splitext(wav)[0] + '.apk'
            if (apk_name == apk):
                print("LogDagg-> ", apk_name, " = ", apk)
                Continue = True
                break
        if (Continue == True):
            continue
        else:
            apk_folder_files.append(wav)
'''
# print("\nApk_Folder_Files-> ", apk_folder_files, "\nLength: ", len(apk_folder_files))
'''
per avre la lista dei nomi senza doverli copiare uino ad uno
'''
'''
print(str(wav.split(".")[0]),
      end=",")  # TODO: levare lo split perché ci sono i trusted con il punto aggiornare il wavextract

for i in range(0, 2000):
    print(i, end=",")
'''
