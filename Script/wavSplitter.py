'''
wav splitter:
Lo script da realizzare prende in input i file .wav dalla cartella (apk > audio > trusted) e suddivide il file in più
file della durata data in input?
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
@splittingduration: la variabile a cui viene assegnato il valore in cui splittare il file .wav
'''
splittingduration = 0
while ((type(splittingduration) != float) or (splittingduration < 0)):
    splittingduration = input("Splittingduration (Seconds): ")
    print("\n")
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

print("Log  -> trusted_audio", trusted_audio, "\n")

createNewDirectory(audio_folder, "Splitted_Wav")
SplittedDir = os.path.join(audio_folder, "Splitted_Wav")

# Itera su tutti i file .wav nella cartella trusted_audio
for wav_file in os.listdir(trusted_audio):
    if wav_file.endswith(".wav"):
        print("wav_Files-> ", wav_file)
        # creo la sottocartella dove inserirò il file audio suddiviso
        wavSplittedDirectory = createNewDirectory(SplittedDir, str(wav_file))
        print("LOG-> ", wavSplittedDirectory)
        pathToOriginalWav = trusted_audio + "\\" + str(wav_file)

        # TODO: suddividere il file audio
        # TODO: calcolare la divisione
        t1 = 0 * 1000  # Works in milliseconds
        t2 = splittingduration * 1000
        newAudio = AudioSegment.from_wav(pathToOriginalWav)
        print("LOG-> original Audio duration seconds: ", newAudio.duration_seconds, " Minutes: ",
              (newAudio.duration_seconds / 60), " Hours: ", ((newAudio.duration_seconds / 60) / 60))

        newAudio = newAudio[t1:t2]
        newAudio.export(out_f=wavSplittedDirectory + "\\" + str(t1) + " - " + str(t2) + '.wav', format="wav")  # Exports
