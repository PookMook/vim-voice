import speech_recognition as sr
from pocketsphinx import LiveSpeech
from pynput.keyboard import Key, Controller
import time

# Create a Controller object from pynput.keyboard
keyboard = Controller()

# Create a LiveSpeech object
speech = LiveSpeech()

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

s2t_active = False
s2t_spelling = False
s2t_uppercase = False
s2t_escape = False
s2t_escape_word = "maria"

def parse_phrase(phrase):
    for word in phrase.split():
        control_listen(word)

def control_listen(word):
    global s2t_active, s2t_uppercase, s2t_escape, s2t_escape_word
    if(s2t_active == False):
        if word == s2t_escape_word and s2t_escape == False:
            print("escaping")
            s2t_escape = True
        if word == "listen" and s2t_escape == False:
            print("listening")
            s2t_active = True;
        else:
            if word == "stop" and s2t_escape == False:
                print("stopped")
                s2t_active = False
            elif word == "uppercase" and s2t_escape == False:
                s2t_uppercase = True
            else:
                control_spell(word)

def control_spell(word):
   global s2t_spelling, s2t_escape
   if s2t_spelling == True:
      if word == "exit" and s2t_escape == False:
         print("end spelling")
         s2t_spelling = False
      else:
         spell(word)
   elif word == "spell" and s2t_escape == False:
      print("spelling")
      s2t_spelling = True
   else:
      type_word(word)

def spell(word):
    global s2t_uppercase
    military_alphabet = {
        "alpha": "a",
        "bravo": "b",
        "charlie": "c",
        "delta": "d",
        "echo": "e",
        "foxtrot": "f",
        "golf": "g",
        "hotel": "h",
        "india": "I",
        "juliet": "j",
        "kilo": "k",
        "lima": "l",
        "mike": "m",
        "november": "n",
        "oscar": "o",
        "papa": "p",
        "quebec": "q",
        "romeo": "r",
        "sierra": "s",
        "tango": "t",
        "uniform": "u",
        "victor": "v",
        "whiskey": "w",
        "x-ray": "x",
        "yankee": "y",
        "zulu": "z",
        "space": " ",
        "paren": "()",
        "bracket": "[]",
        "curly": "{}",
        "coma": ",",
        "dot": ".",
        "quote": "\"",
        "tick": "'",
        "column": ":",
        "semi": ";",
        "bang": "!",
        "at": "@",
        "pound": "#",
        "dollar": "$",
        "percent": "%",
        "caret": "^",
        "amp": "&",
        "start": "*",
        "dash": "-",
        "underscore": "_",
        "plus": "+",
        "equal": "=",
        "pipe": "|",
        "question": "?",
        "slash": "/",
        "less": "<",
        "greater": ">",
        "backslash": "\\",
        "enter": "\n",
        "tilde": "~",
        "back": "`",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0"
    }
    if word == "escape":
        print("press escape")
        keyboard.press(Key.esc)
    else:
        print("keypess: " + military_alphabet.get(word, "unknown"))
        char = military_alphabet.get(word, "")
        if s2t_uppercase == True and char != "":
            char = char.upper()
            s2t_uppercase = False
        keyboard.type(char)

def type_word(word):
        global s2t_uppercase, s2t_escape
        if s2t_uppercase == True:
            word = word.title()
            s2t_uppercase = False
        s2t_escape = False
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

