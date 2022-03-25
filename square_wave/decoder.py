import winsound
import math
import wave
import struct
import re

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

#this will extract an array of numerical values representing 1s and 0s
def find_elements(speed, frames):
    frames = chunks(frames,8 * speed)
    result = []
    for frame in frames:
        try:
            if frame[0] == frame[1] == frame[2] == frame[3] == frame[4] == frame[5] == frame[6] == frame[7]:
                result.append(frame[0])
        except:
            pass
    return result


def decode_binary(frames):
    one = max(frames)
    zero = min(frames)
    result = ''
    for frame in frames:
        if frame == one:
            result = result + '1'
        elif frame == zero:
            result = result + '0'
    return result

def binary_to_text(text):
    return bytes(int(b, 2) for b in re.split('(........)', text) if b).decode('utf8')

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    #Code for if the script isn't imported as a library
    filename = input('WAV filename: ')
    speed = int(input('Lenght in ms of a single bit in the wav file: '))
    print('Decoding Result:')
    frames = get_frames(filename)
    elements = find_elements(speed,frames)
    try:
        result = decode_binary(elements)
    except:
        print('No binary square wave in .wav file found')
        input("Press any key to continue...")
        exit()
    try:
        text = binary_to_text(result)
        print(text)
        with open(filename.replace('.wav','.txt'), 'w') as f:
            f.write(text)
    except:
        print('Decoding binary to text failed...')
        print('Extracted binary from .wav file saved to txt file')
        with open(filename.replace('.wav','.txt'), 'w') as f:
            f.write(result)
    input("Press any key to continue...")
