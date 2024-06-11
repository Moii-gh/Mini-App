import speech_recognition as sr
import pyaudio
import webbrowser

recognizer = sr.Recognizer()
def search_google():
    with sr.Microphone() as sourse:
        print("Говори чета")
        try:
            audio = recognizer.listen(sourse)
            query = recognizer.recognize_google(audio, language = "ru- RU")
            print(f"Вы сказали {query}")
            search_url = f"https://yandex.ru/search/?text={query}"
            print(search_url)
            webbrowser.open(search_url)
        except sr.UnknownValueError:
            print("Ну капец")

search_google()


