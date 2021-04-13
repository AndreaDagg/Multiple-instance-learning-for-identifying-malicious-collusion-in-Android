import os
import zipfile
import sys
import wave
import struct

# Legge i file .apk presenti in /Users/nicola/Desktop/tesi/apk e
# li converte in file .wav nella cartella /Users/nicola/Desktop/tesi/apk/audio

'''
@convert_flie_to_wav: Prende in input un file da convertire e ritorna un file di tipo (...) 
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
        header = struct.pack("%sB" % len(header), *header)
        header += struct.pack("<HH", len(data), len(data))
        data = header + data + struct.pack("<L", sum(data))

    return data


'''
@bits: L'array bits di esadecimali forma un'onda (non sinusoidale) dato che i valori si ripetono ma con ampiezza diverse
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
    bits[0] = [b ^ 0x80 for b in bits[0]]
    bits[1] = [b ^ 0x80 for b in bits[1]]
    bits[0] = struct.pack("%sB" % len(bits[0]), *bits[0])
    bits[1] = struct.pack("%sB" % len(bits[1]), *bits[1])
    open("test.bin", "wb").write(data)

    wav_out = wave.open(path, "w")
    wav_out.setparams((1, 1, 32768, 0, "NONE", "not compressed"))

    for v in data:
        for i in range(8):
            wav_out.writeframes(bits[(v >> i) & 1])

    wav_out.close()


# Base_path = /Users/nicola/Desktop/tesi
base_path = os.getcwd()
apk_folder = os.path.join(base_path, "apk")
trusted_apk = os.path.join(apk_folder, "trusted")
malware_apk = os.path.join(apk_folder, "malware")

audio_folder = os.path.join(apk_folder, "audio")
trusted_audio = os.path.join(audio_folder, "trusted")
malware_audio = os.path.join(audio_folder, "malware")

if not os.path.exists(audio_folder):
    os.mkdir(audio_folder)

# Conversione da apk/trusted/file.apk a apk/audio/trusted/file.wav
print(apk_folder)
apk_folder_files = list()
for apk in os.listdir(trusted_apk):
    if apk.endswith(".apk"):
        apk_folder_files.append(apk)

print(apk_folder_files)

for apk in apk_folder_files:
    print("Current apk: ", apk)
    apk_path = os.path.join(trusted_apk, apk)
    print(apk_path)
    archive = zipfile.ZipFile(apk_path, "r")
    try:
        dex_file = archive.read("classes.dex")

        # Conversione del file dex in .wav
        audio_file = convert_file_to_wav(dex_file)

        # Prendo nome.apk e lo trasformo in nome.wav
        wav_name = os.path.splitext(apk)[0] + '.wav'
        wav_path = os.path.join(trusted_audio, wav_name)

        # Salvo nome.wav nella cartella /apk/audio
        wav_to_file(audio_file, wav_path)

        audio_file

    except KeyError:
        print("     APK non contiene il file classes.dex")
