import winsound
import math
import wave
import struct

def string_into_binary(input):
    binary_result = ''.join('{:08b}'.format(b) for b in input.encode('utf8'))
    return binary_result

def generate_audio(data, speed, total_volume):
    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    audio = []
    sample_rate = 8000
    for char in data:
        if char == '0':  
            num_samples = speed * (sample_rate / 1000.0)
            for x in range(int(num_samples)):
                audio.append(total_volume * 0.5)
        elif char == '1': 
            num_samples = speed * (sample_rate / 1000.0)
            for x in range(int(num_samples)):
                audio.append(total_volume)
    return audio

def save_wav(filename,audio):

    sample_rate = 8000

    wav_file=wave.open(filename,"w")

    nchannels = 1

    sampwidth = 2

    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

if __name__ == "__main__":
    #Code for if the script isn't imported as a library

    speed = 1 #how long sounds for 1 and 0 last
    total_volume = 1 #Base volume
    filename = 'result_'

    #gather user text input, if user input is a txt file name try opening that file
    user_input = input('Input text or txt file name next to the script: ')
    if user_input.endswith(".txt"):
        try:
            with open(user_input) as f:
                filename = user_input.replace('.txt','') + '_'
                user_input = str(f.read())
        except:
            print('File not found')

    #turn that input into binary
    data = string_into_binary(user_input)
    print('Data converted into binary. Result: ' + data)
    audio = generate_audio(data,speed,total_volume)
    print('Audio generated')
    save_wav(filename + str(speed) + 'ms.wav',audio)
    print('Audio saved to file')
    input("Press any key to continue...")
