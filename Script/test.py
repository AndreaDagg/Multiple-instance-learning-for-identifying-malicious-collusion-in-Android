import os
import zipfile
import sys
import wave
import struct

# Legge i file .apk presenti in /Users/nicola/Desktop/tesi/apk e
# li converte in file .wav nella cartella /Users/nicola/Desktop/tesi/apk/audio


'''
if true significa che stiamo convertendo gli apk del dataset Trusted
If false significa che stiamo convertendo gi apk del dataset ACID
'''
DatasetType = True
Test_APk = True

'''
@convert_flie_to_wav:   Prende in input un file da convertire e ritorna un file di tipo (...) 
                        Il parametro mode è impostato a raw di default, se non esplicitato nel richiamo della funzione resterà come di default 
'''


def convert_file_to_wav(file_to_convert, mode="raw"):
    data = file_to_convert

    '''
    @header array di esadecimali (string),  dove 0xAA   = (A * 16^0) + (A * 16^1) -> 170   (decimale) = 10101010 (binario) 
                                            dove 0x0A   = (A * 16^0) + (0 * 16^1) -> 10    (decimale) = 00001010 (binario)
                                            dove 0x02   = (2 * 16^0) + (0 * 16^1) -> 2     (decimale) = 00000010 (binario)
    '''
    if mode == "level":
        header = [
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0xAA,
            0x0A,
            0x02,
            0x02,
        ]
        '''
        @struct.pack:   Restituisce una stringa contenente tutti i valori di header, che sono impacchettati in base al formato passato come primo parametro
                        (le stringhe di formato sono il meccanismo utilizzato per specificare il layout previsto quando si comprimono e scompattano i dati). 
                        I valori seguiti dal formato devono essere come da solo formato, altrimenti viene sollevato struct.error.
                        Il carattere * consente a header di scorrere tutti i suoi elementi. 
                        Gli argomenti devono corrispondere esattamente ai valori richiesti dal formato.
        '''
        header = struct.pack("%sB" % len(header), *header)
        # print("log-->", header)
        header += struct.pack("<HH", len(data), len(data))
        data = header + data + struct.pack("<L", sum(data))
    # else:
    # print("Logdagg -> non mode level in convert file to wav function") #TODO Cancella

    return data


'''
@data: File convertito da file .dex in .wav   
@path: La path i-esima dove si trova la Directory apk a cui è stata cambiata l'estensione in .wav
---
@bits: La matrice 2 * 32 bits di esadecimali forma un'onda (non sinusoidale) dato che i valori si ripetono ma con ampiezza diverse
'''


def wav_to_file(data, path):
    bits = [
        [
            0x00,  # 0
            0x09,  # 9  01001
            0x12,  # 18 10010
            0x1A,  # 26 11010
            0x21,  # 33 100001
            0x27,  # 39 100111
            0x2C,  # 44 101100
            0x2F,  # 47 101111
            0x30,  # 48 110000
            0x2F,  # 47 101111
            0x2C,  # 44 101100
            0x27,  # 39 100111
            0x21,  # 33 100001
            0x1A,  # 26 11010
            0x12,  # 18 10010
            0x09,  # 9  01001
            0x00,  # 0
            0xF6,
            0xED,
            0xE5,
            0xDE,
            0xD8,
            0xD3,
            0xD0,
            0xD0,
            0xD0,
            0xD3,
            0xD8,
            0xDE,
            0xE5,
            0xED,
            0xF6,
        ],
        [
            0x00,
            0x18,
            0x30,
            0x46,
            0x59,
            0x69,
            0x75,
            0x7C,
            0x7F,
            0x7C,
            0x75,
            0x69,
            0x59,
            0x46,
            0x30,
            0x18,
            0x00,
            0xE7,
            0xCF,
            0xB9,
            0xA6,
            0x96,
            0x8A,
            0x83,
            0x81,
            0x83,
            0x8A,
            0x96,
            0xA6,
            0xB9,
            0xCF,
            0xE7,
        ],
    ]

    # import numpy as np  # TODO: Cancella
    # print(np.matrix(bits))
    '''
    Operatori bit per bit ^ XOR 
    Per ogni bit nella riga della matrice bit vine emesso in XOR con 0x80 -> 128 -> 10000000
    La matrice bit diventa una matrice di XOR
    ----
    
    '''
    bits[0] = [b ^ 0x80 for b in bits[0]]
    bits[1] = [b ^ 0x80 for b in bits[1]]

    #  print("\n", np.matrix(bits))  # TODO: Cancella

    # TODO: Capire
    bits[0] = struct.pack("%sB" % len(bits[0]), *bits[0])
    bits[1] = struct.pack("%sB" % len(bits[1]), *bits[1])

    # print("\n", np.matrix(bits))  # TODO: Cancella
    '''
    @open:              Crea un file per la scrittura 'W' && 'b' binary mode quindi 'wb' indica che il file è aperto per la scrittura in modalità binaria.
                        Nel file creato scrive il File convertito da file .dex in .wav 
    @wave.open:         Apre il file in modalità scrittura
    @wave.setparams:    (nchannels, sampwidth, framerate, nframes, comptype, compname)
    @wave.writeframes:  Scrivi fotogrammi (frame) audio.
                        >>  operations Spostamento a destra. Sposta a destra spingendo le copie del bit più a sinistra da sinistra e lasciare cadere i bit più a destra
                        &   AND logico 
    '''
    open("test.bin", "wb").write(data)

    wav_out = wave.open(path, "w")
    wav_out.setparams((1, 1, 32768, 0, "NONE", "not compressed"))

    for v in data:
        for i in range(8):
            wav_out.writeframes(bits[(v >> i) & 1])

    wav_out.close()


# Base_path = /Users/nicola/Desktop/tesi
'''
@getcwd:    restituisce la directory di lavoro corrente
@path.join: unisce uno o più componenti del percorso. Concatena vari componenti del percorso con esattamente un separatore di directory ('/') dopo ogni parte non vuota tranne l'ultimo componente del percorso.
'''
# TODO: Si potrebbe controllare se le cartelle esistono o crearle via codice os.makedirs("C:\\nuova__cartella")

base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")
trusted_apk = os.path.join(apk_folder, "trusted")
malware_apk = os.path.join(apk_folder, "malware")
test_apk = os.path.join(apk_folder, "Test_Apk")
acid_apk = os.path.join(apk_folder,"trusted_Acid")

'''
print("\n------------------------- START LogDag-----------------------", "\nLogDag-> Base: ", base_path,
      "\nLogDag-> Apk_Folder ", apk_folder, "\nLogDag-> Trusted_Apk ", trusted_apk, "\nLogDag-> Malware Apk ",
      malware_apk, "\n------------------------- END LogDag-----------------------\n")
'''

audio_folder = os.path.join(apk_folder, "audio")
trusted_audio = os.path.join(audio_folder, "trusted")  # cartella di destinazione dei file .apk dataset acid
malware_audio = os.path.join(audio_folder, "malware")
trusted_audio_trusted_apk = os.path.join(audio_folder,
                                         "trusted_audio_trusted_apk")  # cartella di destinazione dei file .apk trusted
#Crea la cartella di testing
import wavDatasetLib
wavDatasetLib.createNewDirectory(audio_folder, "trusted_audio_Test_apk")
trusted_audio_Test_apk = os.path.join(audio_folder, "trusted_audio_Test_apk")

# Crea la cartella audio_folder se non esiste nella (...)
if not os.path.exists(audio_folder):
    os.mkdir(audio_folder)
    print("LogDagg -> audio_folder Create")
else:
    print("LogDagg -> audio_folder Not Create")

# Conversione da apk/trusted/file.apk a apk/audio/trusted/file.wav
print("Apk_Folder path-> ", apk_folder)
apk_folder_files = list()  # inizializza una lista/array
'''
Contollo If se stiamo convertendo gli apk del dataset acid oppure trusted, oppure trusted ma con apk di testing per la cartella di output

Itera sui file presenti nella cartella trustes_apk e se un file all'iterata (apk-esima) termina con .apk lo aggiunge alla directory apk_folder_files 
@os.listdir:    restituisce una lista contenente i nomi delle voci nella directory data da path. L'elenco è in ordine arbitrario. Non include le voci speciali "." e '..' anche se sono presenti nella directory.

Aggiunta codice per controllare se l'apk è gia stato convertito, in modo che vengano aggiunti alla lista @apk_folder_files solo i file da convertire nuovi
'''

if (DatasetType and Test_APk):
    destinationFolderWav = trusted_audio_Test_apk
    inputFolder = test_apk
elif (DatasetType and (Test_APk == False)):
    destinationFolderWav = trusted_audio_trusted_apk
    inputFolder = trusted_apk
else:
    destinationFolderWav = trusted_audio  # TODO: Rinominare la cartella in Acid_audio
    inputFolder = acid_apk

for apk in os.listdir(inputFolder):
    Continue = False
    if ((apk.endswith(".apk"))):
        for wav in os.listdir(destinationFolderWav):
            # print("LogDagg-> Trusted audio: ", trusted_audio)
            wav_name = os.path.splitext(apk)[0] + '.wav'
            if (wav_name == wav):
                print("LogDagg-> wawModify: ", wav_name, " = ", wav)
                Continue = True
                break
        if (Continue == True):
            continue
        else:
            apk_folder_files.append(apk)

print("\nApk_Folder_Files-> ", apk_folder_files, "\nLength: ", len(apk_folder_files))
print("\n DATASET TRUSTED: ", DatasetType)

'''
@zipfile.ZipFile:   prende in input la path dell'i-esimo apk della cartella e mode = "r" 
                    'r' leggere un file esistente, 'w' troncare e scrivere un nuovo file, 'a' aggiungere a un file esistente o 'x' creare e scrivere esclusivamente un nuovo file.
                    -> Quidni archive va a leggere(decomprimere) il file .apk i-esimo
@archive.read:      ZipFile.read() Restituisce i byte del nome del file nell'archivio. nome è il nome del file nell'archivio o un ZipInfooggetto. L'archivio deve essere aperto per la lettura o l'aggiunta. pwd è la password utilizzata per i file crittografati

@os.path.splitext:  Passa come parametro la path dell'apk e divide il nome del percorso in una coppia root ed extension root è tutto tranne la parte .extension. 
                    /home/User/Desktop/file.txt (path)    /home/User/Desktop/file  (root)            .txt (ext)
                    Restiruisce una coppia [0] la root [1] l'estensione
'''
iteration = 1
for apk in apk_folder_files:
    print("\nCurrent apk: ", apk, "\nIter: ", iteration)
    iteration += 1  # LOG iterazione per tenere traccia dell'apk
    apk_path = os.path.join(inputFolder, apk)  # path dell'apk i-esimo
    # print("Apk Path: ", apk_path)
    archive = zipfile.ZipFile(apk_path, "r")  # Quidni archive va a leggere(decomprimere) il file .apk i-esimo
    try:
        dex_file = archive.read("classes.dex")  # Legge il file classes.dex presente nell'archvio .apk

        # Conversione del file dex in .wav
        audio_file = convert_file_to_wav(dex_file)

        '''
        @trusted_audio: Script/apk/audio/trusted
        @wav_name:      i-esima Directory apk a cui è stata cambiata l'estensione in .wav
        @wav_path:      Script/apk/audio/trusted/wav_name.wav    
        @audio_file:    Conversione del file dex in .wav   
        '''
        # Prendo nome.apk e lo trasformo in nome.wav
        # modifica l'estensuione andando ad aggiungere alla root [0] della path ".wav"
        wav_name = os.path.splitext(apk)[0] + '.wav'
        '''
        Il primo se elaboriamo gli apk del dataset acid
        Il secodno de elaboriamo gli apk del dataset trusted
        il terzo wav_path gestisce in automatico con una variabile globale definita precendentemente
        '''
        # wav_path = os.path.join(trusted_audio, wav_name)
        # wav_path = os.path.join(trusted_audio_trusted_apk, wav_name)

        wav_path = os.path.join(destinationFolderWav, wav_name)

        # Salvo nome.wav nella cartella /apk/audio
        wav_to_file(audio_file, wav_path)

        audio_file

    except KeyError:
        print("     APK non contiene il file classes.dex")
