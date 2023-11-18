import speech_recognition as sr
from pocketsphinx import LiveSpeech
from pynput.keyboard import Controller
import time

# Create a Controller object from pynput.keyboard
keyboard = Controller()

# Create a LiveSpeech object
speech = LiveSpeech()

s2t_active = False

mic_name = 'HDA Intel PCH: ALC1150 Analog (hw:1,0)'
mic_list = sr.Microphone.list_microphone_names()
device_id = 1
for i, microphone_name in enumerate(mic_list):
    print(microphone_name)
    if microphone_name == mic_name:
        device_id = i
print('DEVICE >>')
print(mic_name)
print(device_id)


def parse_phrase(phrase):
    global s2t_active
    for word in phrase.split():
        if(s2t_active == False):
            if word == "listen":
                print("listening")
                s2t_active = True;
        else:
            if word == "stop":
                print("stopped")
                s2t_active = False
            else:
                type_word(word)

def type_word(word):
        keyboard.type(word)
        keyboard.press(' ')
        keyboard.release(' ')
        # Pause for a while to simulate typing speed
        time.sleep(0.1)

r = sr.Recognizer()
with sr.Microphone(device_index = device_id, sample_rate = 44100, chunk_size = 512) as source:
    r.adjust_for_ambient_noise(source)
    print('openmic')
    while True:
        print("mic loop")
        audio = r.listen(source)
        try:
            phrase = r.recognize_sphinx(audio)
            print('you said:' + phrase)
            parse_phrase(phrase)
        except sr.UnknownValueError as e:
            print('could not recognize {0}'.format(e))
        except Exception as e:
            print("error: {0}".format(e))

