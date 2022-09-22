import keyboard 
import pyaudio

def textToBinary(string):
    return ''.join(format(ord(x), 'b') for x in string)

#recording config
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
total_volume = 100
speed = 0.125

#i decided to precede each transmition with the actual encoded wav file header
#https://docs.fileformat.com/audio/wav/ 
#the text is encoded in ASCII
RIFF = '01010010010010010100011001000110' #first element of header - static
WAVE = '01010111010000010101011001000101' #third element - static
FMT_ = '01000110010011010101010000000000' #fourth element - static
LENG = '00000000000000000011000100110110' #fifth element - tells how much following bytes contain format info
TYPE = '0000000000000010' #sixth element - tells if encoded in PCM or INT16, in our case int16 so the value is 2 as int16
CHANNEL = str('{:016b}'.format(CHANNELS)) #seventh element - tells how many channels are encoded as int16
SAMPLE_RATE = str('{:032b}'.format(RATE)) #eight element - tells the sample rate as int32
#now he have a bunch of space for stuff i can't be bothered to encode so here we go 8 empty bytes
EMPTY = '00000000' * 6
BITS = '0011000100110110' #bits per sample - in this case 16
DATA = '01000100010000010101010001000001' #static marker

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True, output=True,
                frames_per_buffer=CHUNK)

print('Press space to transmit')
while True:  # making a loop
    if keyboard.is_pressed('space'):  # if key 'space' is pressed 
        data = stream.read(CHUNK)
        int_values = [x for x in data]
        arr = []
        for value in int_values:   
            arr.append('{:08b}'.format(value))
        header = RIFF + '{:032b}'.format((len(arr) + 352)) + WAVE + FMT_ + LENG + TYPE + CHANNEL + SAMPLE_RATE + EMPTY + BITS + DATA + '{:032b}'.format(len(arr))
        bits = header + ''.join(arr)
        audio = []
        for value in bits :
            num_samples = speed * (RATE / 1000.0)
            if value == '0':
                for x in range(int(num_samples)):
                    audio.append(int(total_volume/2))
            else:
                for x in range(int(num_samples)):
                    audio.append(total_volume)
        stream.write(bytes(audio))
    elif keyboard.is_pressed('ctrl'):
        print('Halting...')
        break

