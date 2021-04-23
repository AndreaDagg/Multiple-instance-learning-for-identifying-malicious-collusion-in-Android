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

apk_folder_files = list()
for wav in os.listdir(trusted_audio):
    '''
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
    #print(str(wav), end=",")
