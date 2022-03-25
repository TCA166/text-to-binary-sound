import winsound
import math
import wave
import struct
import re

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def check_sinewave(frames):
    #get maximum and minimum pitch values
    maxima = max(frames)
    minima = min(frames)
    #a proper and constistent sinewave will always have maximum and minimum values that when added make 0
    return (maxima + minima) == 0

def frames_into_binary(frames, speed):
    frames_split = list(chunks(frames,8 * speed))
    zeroes = []
    for element in frames_split:
        zeroes.append(element.count(0))
    #here we assume one will be represented as a sinewave with higher frequency than zero
    one = max(zeroes)
    zero = min(zeroes)
    for i in range(0, len(zeroes)):
        zeroes[i] = str(zeroes[i]).replace(str(zero),'0').replace(str(one),'1')
    zeroes = ''.join(zeroes)
    return zeroes

def get_frames(filename):
    #unpack wavefile frames into an array of ints containing pitch values
    file = wave.open(filename,mode='rb')
    length = file.getnframes()
    frames = []
    for i in range(0, length):
        wavedata = file.readframes(1)
        data = struct.unpack("<h", wavedata)
        frames.append(int(data[0]))
    return frames

def binary_to_text(text):
    return bytes(int(b, 2) for b in re.split('(........)', text) if b).decode('utf8')

if __name__ == "__main__":
    #Code for if the script isn't imported as a library
    filename = input('WAV filename: ')
    speed = int(input('Lenght in ms of a single bit in the wav file: '))

    frames = get_frames(filename)

    if check_sinewave(frames): 
        binary = frames_into_binary(frames,speed)
        print(binary_to_text(binary))
    else:
        print("The WAV file doesn't contain a clear sine wave that can be decoded")
    input("Press any key to continue...")
