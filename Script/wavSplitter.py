'''
wav splitter:
Lo script da realizzare prende in input i file .wav dalla cartella (apk > audio > trusted) e suddivide il file in più
file della durata data in input?
'''
import os

'''
@splittingduration: la variabile a cui viene assegnato il valore in cui splittare il file .wav
'''
splittingduration = 0
while ((type(splittingduration) != float) or (splittingduration < 0)):
    splittingduration = input("Splittingduration: ")
    try:
        splittingduration = float(splittingduration)
        print("Log  -> input duration type: ", type(splittingduration), " value: ", splittingduration)
        if (splittingduration < 0):  # il valore dev'essere 0 o maggiore di 0
            print("Invalid negative input")
    except ValueError:
        print("The input data is not a number")

# file .wav path directory
base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")
audio_folder = os.path.join(apk_folder, "audio")
trusted_audio = os.path.join(audio_folder, "trusted")

print("Log  -> trusted_audio", trusted_audio)
