import speech_recognition as sr
import googletrans
from gtts import gTTS
from playsound import playsound
import os

# LANGUAGES
dic={'afrikaans':'af', 'albanian':'sq', 'amharic':'am',
	'arabic':'ar', 'armenian':'hy', 'azerbaijani':'az',
'basque':'eu', 'belarusian':'be', 'bengali':'bn', 'bosnian':
	'bs', 'bulgarian':'bg', 'catalan':'ca',
'cebuano':'ceb', 'chichewa':'ny', 'chinese (simplified)':
	'zh-cn', 'chinese (traditional)': 'zh-tw',
'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish':
	'da', 'dutch': 'nl', 'english': 'en', 'esperanto':
'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi',
	'french': 'fr', 'frisian': 'fy', 'galician': 'gl',
'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati':
	'gu', 'haitian creole': 'ht', 'hausa': 'ha',
'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong':
	'hmn', 'hungarian':'hu', 'icelandic': 'is', 'igbo':
'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it',
	'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn',
'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)':
	'ku', 'kyrgyz': 'ky', 'lao': 'lo',
'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish':
	'lb', 'macedonian':'mk', 'malagasy':
'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori':
	'mi', 'marathi': 'mr', 'mongolian':'mn',
'myanmar (burmese)': 'my', 'nepali':'ne', 'norwegian':'no',
	'odia': 'or', 'pashto': 'ps', 'persian':
'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa',
	'romanian':'ro', 'russian':'ru', 'samoan':
'sm', 'scots gaelic': 'gd', 'serbian':'sr', 'sesotho':
	'st', 'shona':'sn', 'sindhi': 'sd', 'sinhala':
'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali':'so',
	'spanish': 'es', 'sundanese': 'su',
'swahili': 'sw', 'swedish': 'sv', 'tajik':'tg', 'tamil':
	'ta', 'telugu': 'te', 'thai':'th', 'turkish': 'tr',
'ukrainian': 'uk', 'urdu':'ur', 'uyghur': 'ug', 'uzbek':
	'uz', 'vietnamese':'vi', 'welsh': 'cy', 'xhosa': 'xh',
'yiddish':'yi', 'yoruba':'yo', 'zulu': 'zu'}

# SPEECH TO TEXT
def stt(language):
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            info_to_app_language("Listening...")
            audio = r.listen(source)
            try:
                speech_text=r.recognize_google(audio, language=language)
                print(speech_text)
                return speech_text.lower()
            except sr.UnknownValueError:
                info_to_app_language("Could not understand.")
                playsound("command7.mp3")
            except sr.RequestError:
                info_to_app_language("Could not request result from Google. Try again")
                playsound("command8.mp3")
            except ConnectionResetError:
                info_to_app_language("Could not request result from Google. Try again")
                playsound("command8.mp3")

# TRANSLATING WRITTEN TEXT
def translate_text(text_to_translate, destination_lang):
    translator = googletrans.Translator()
    translated_text = translator.translate(str(text_to_translate), dest=destination_lang)
    return translated_text.text

# TEXT TO SPEECH
def tts(text_to_speak, language, filename):
    voice = gTTS(text_to_speak, lang=language)
    voice.save(filename)

# SAVING VOICE COMMANDS IN APP LANGUAGE
def commands():
    if language_app=="en":
        tts("Choose the app language.", "en", "command1.mp3")
        tts("What's the language you want to translate from?", "en", "command2.mp3")
        tts("What's the language you want to translate to?", "en", "command3.mp3")
        tts("You can speak now.", "en", "command4.mp3")
        tts("Do you want to continue?", "en", "command5.mp3")
        tts("Do you want to change the languages?", "en", "command6.mp3")
        tts("Could not understand. Try again", "en", "command7.mp3")
        tts("Could not request result from Google. Try again", "en", "command8.mp3")
    else:
        tts("Choose the app language.", language_app, "command1.mp3")
        tts(translate_text("What's the language you want to translate from?", language_app), language_app, "command2.mp3")
        tts(translate_text("What's the language you want to translate to?.", language_app), language_app, "command3.mp3")
        tts(translate_text("You can speak now.", language_app), language_app, "command4.mp3")
        tts(translate_text("Do you want to continue?", language_app), language_app, "command5.mp3")
        tts(translate_text("Do you want to change the languages?", language_app), language_app, "command6.mp3")
        tts(translate_text("Could not understand. Try again", language_app), language_app, "command7.mp3")
        tts(translate_text("Could not request result from Google. Try again", language_app), language_app, "command8.mp3")

# CHOOSING THE LANGUAGE ACRONYM BY ITS NAME FROM THE DICTIONARY
def choose_language():
    while True:
        language = stt(language_app)
        if language_app!="en":
            language=translate_text(language, "en").lower()
        if language in dic:
            language = dic[language]
            break
        else:
            playsound("command7.mp3")
    return language

# SETTING THE ORIGINAL LANGUAGES AND DESTINATION LANGUAGE IN TRANSLATING
def first_second_language():
    playsound("command2.mp3")
    first = choose_language()
    info_to_app_language("You are going to translate from:")
    print(f"{first}.")
    playsound("command3.mp3")
    second = choose_language()
    info_to_app_language("You are going to translate to:")
    print(f"{second}.")
    return first, second

# VOICE TRANSLATOR
def translation(first_language, second_language):
    playsound("command4.mp3")
    speech_text = stt(str(first_language))
    speech_text = translate_text(speech_text, str(second_language))
    print(speech_text)
    tts(speech_text, str(second_language), "voice.mp3")
    playsound("voice.mp3")
    os.remove("voice.mp3")

# TRANSLATING INFORMATION FOR USER SHOWN ON THE SCREEN TO THE APP LANGUAGE
def info_to_app_language(info):
    if language_app != "en":
        info = translate_text(info, language_app)
    print(info)

# MAIN
language_app="en"
commands()
playsound("command1.mp3")
language_app=choose_language()
print(f"{language_app}", end = ' ')
info_to_app_language("is your app language")
commands()

first_loop=True

while True:
    if first_loop==False: # EVERY TIME THE USER CAN CHANGE THE LANGUAGES
        playsound("command6.mp3")
        answer = stt(language_app)
        if answer == translate_text("yes", language_app).lower():
            first_language, second_language = first_second_language()
        else:
            info_to_app_language("You are going to translate from:")
            print(f"{first_language}.")
            info_to_app_language("You are going to translate to:")
            print(f"{second_language}.")
    else:
        first_language, second_language = first_second_language()
    translation(first_language, second_language)
    playsound("command5.mp3")
    answer = stt(language_app)
    if answer != translate_text("yes", language_app).lower():
        break
    info_to_app_language("Continuing...")
    first_loop = False

os.remove("command1.mp3")
os.remove("command2.mp3")
os.remove("command3.mp3")
os.remove("command4.mp3")
os.remove("command5.mp3")
os.remove("command6.mp3")
os.remove("command7.mp3")
os.remove("command8.mp3")


