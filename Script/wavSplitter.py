'''
wav splitter:
Lo script da realizzare prende in input i file .wav dalla cartella (apk > audio > trusted) e suddivide il file in più
file della durata data in input.

Lo script chiede in input la durata dello split in secondi.
Se non è stata creata va a creare una cartella Splitted_Wav in apk > audio > Splitted_wav  tramite una funzione “createNewDirectory”.
Proseguendo va ad iterare su tutti i file .wav in apk > audio > trusted
e per ogni .wav trovato crea una sub directory in apk > audio > Splitted_wav che prende il nome del file .wav da splittare e va poi a popolarla dei file splittati.
Ho pensato di fare in questo modo così ogni file .wav avrà una sua cartella che conterrà gli split.
Lo split l’ho fatto in una funzione “splittingWav” che va a calcolare il numero degli split in cui suddividere il file audio originale e poi itera sugli intervalli e crea la suddivisione sempre però partendo dal file originale.
Ho usato però una libreria per fare lo split che si chiama “pydub”.
------------------------------------ LIBRERIE -------------------------------------------
-   pip install pydub
-   scaricare ffmpeg https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z
    Estrarlo in una directory e aggiungere le path alle variabili di ambiente windows
    pip install ffmpeg
'''
import os
from pydub import AudioSegment

# https://github.com/jiaaro/pydub#installation
# ffmpeg https://www.gyan.dev/ffmpeg/builds/
# Come aggiungere ffmpeg https://github.com/jiaaro/pydub/issues/348
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
La funziona splittingWav prende in input 
@pathToOriginalWav:     La path al file .wav originale da splittare
@pathToSplittedWav:     La path alla directory in cui si salveranno i file splittati
@splittingsuration:     Variabile globale data in input, rappresenta la durata dei file splittati
@originalAudio:         Il file .wav da splittare

Calcola tramite una divisione per eccesso il numero intero di split da effettuare per dividere il file .wav 
Le variabili @t_start e @t_stop rappresentano per ogni iterata il punto d'inizio e quello di fine dell'iesimo split del file
'''


def splittingWav(pathToOriginalWav, pathToSplittedWav):
    originalAudio = AudioSegment.from_wav(pathToOriginalWav)

    print(
        "\n----------------------- Splitting -------------------------------\n LOG-> original Audio duration seconds: ",
        originalAudio.duration_seconds, " Minutes: ",
        (originalAudio.duration_seconds / 60), " Hours: ", ((originalAudio.duration_seconds / 60) / 60), "\n\n")

    # divisione per eccesso (estremo superiore)
    numberOfSplit = round(originalAudio.duration_seconds / splittingduration)
    # numberOfSplit = 10

    print("LOG-> Number of split: ", numberOfSplit)

    t_start = 0
    for i in range(numberOfSplit):
        t_stop = (t_start + (splittingduration * 1000))  # Works in milliseconds
        print(F"Passo {i} \n t_start {t_start}, t_stop {t_stop}")
        splittedAudio = originalAudio[t_start:t_stop]
        splittedAudio.export(out_f=pathToSplittedWav + "\\" + str(t_start) + " - " + str(t_stop) + '.wav',
                             format="wav")  # Exports
        t_start = t_stop


'''
- Get positive split duration
@splittingsuration:     Variabile globale data in input, rappresenta la durata dei file splittati
'''
splittingduration = 0
while ((type(splittingduration) != float) or (splittingduration <= 0)):
    splittingduration = input("Splittingduration (Seconds): ")
    try:
        splittingduration = float(splittingduration)
        print("Log  -> input duration type: ", type(splittingduration), " value: ", splittingduration)
        if (splittingduration < 0 or splittingduration == 0):  # il valore dev'essere 0 o maggiore di 0
            print("The duration of the split cannot be zero or less than zero")
    except ValueError:
        print("The input data is not a number")

# file .wav path directory
base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")
audio_folder = os.path.join(apk_folder, "audio")
trusted_audio = os.path.join(audio_folder, "trusted")

print("Log  -> trusted_audio", trusted_audio, "\n")

createNewDirectory(audio_folder, "Splitted_Wav")
SplittedDirectory = os.path.join(audio_folder, "Splitted_Wav")  # path alla dierctory dei file splitted

# Itera su tutti i file .wav nella cartella trusted_audio
for wav_file in os.listdir(trusted_audio):
    if wav_file.endswith(".wav"):
        print("wav_Files-> ", wav_file)
        # creo la sottocartella dove inserirò il file audio suddiviso
        wavSplittedDirectory = createNewDirectory(SplittedDirectory, str(wav_file))
        print("LOG-> ", wavSplittedDirectory)
        pathToOriginalWav = trusted_audio + "\\" + str(wav_file)  # path to original file .wav
        splittingWav(pathToOriginalWav, wavSplittedDirectory)
