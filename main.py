import speech_recognition as sr
from pocketsphinx import LiveSpeech
from pynput.keyboard import Controller
import time

# Create a Controller object from pynput.keyboard
keyboard = Controller()

# Create a LiveSpeech object
speech = LiveSpeech()

mic_name = 'HDA Intel PCH: ALC1150 Analog (hw:1,0)'
mic_list = sr.Microphone.list_microphone_names()
for i, microphone_name in enumerate(mic_list):
    print(microphone_name)
    if microphone_name == mic_name:
        device_id = i
print('DEVICE >>')
print(mic_name)
print(device_id)

r = sr.Recognizer()
with sr.Microphone(device_index = device_id, sample_rate = 44100, chunk_size = 512) as source:
    while True:
        print('listening')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            phrase = r.recognize_sphinx(audio)
            print('you said:' + phrase)
            type_phrase(phrase)
            #keyboard.type(phrase)
            #keyboard.type(" ")
        except sr.UnknownValueError as e:
            print('could not recognize {0}'.format(e))
        except Exception as e:
            print("error: {0}".format(e))
def type_phrase(phase):
    # For each word in the phrase
    for word in phrase.segments():
        keyboard.type(word[0])
        # Simulate pressing the space key to separate words
        keyboard.press(' ')
        keyboard.release(' ')
        # Pause for a while to simulate typing speed
        time.sleep(0.1)

