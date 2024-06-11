import hashlib
import requests
import speech_recognition as sr
import logging
from telebot import TeleBot, logger
import soundfile as sf


Tg_Key = " "
Voice_Lang = "ru-RU"
max_message_size = 50 * 1024 * 1024
max_message_duration = 120
bot = TeleBot(Tg_Key)

@bot.message_handler(commands=["start"])
def start_promt(message):
    reply = " ".join(["Говори в микро или перешли сообщение"])
    return bot.reply_to(message, reply)

@bot.message_handler(content_types=["voice"])
def echo_voice(message):
    data = message.voice
    if(data.file_size > max_message_size) or (data.duration > max_message_duration):
        reply = " ".join(["иди отсюда вон", "сообщение слишком большое"])
        return bot.reply_to(message, reply)
    file_url = "https://api.telegram.org/file/bot{}/{}".format(bot.token, bot.get_file(data.file_id).file_path)
    file_path = download_file(file_url)
    convert_to_pcm16(file_path)
    text = proggres_audio_file("new.wav")

    if not text:
        return bot.reply_to(message, "Не понял что вы сказали")
    return bot.reply_to(message, text)

def download_file(file_url):
    file_path = "voice_message.ogg"
    with open(file_path, "wb") as f:
        response = requests.get(file_url)
        f.write(response.content)
        return file_path

def convert_to_pcm16(file_path):
    data, samplerate = sf.read(file_path)
    data = (data * 32767).astype('int16')
    sf.write('new.wav', data, samplerate)

def proggres_audio_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio_data, language=Voice_Lang)
        return text
    except sr.UnknownValueError:
        return None

logger.setLevel(logging.DEBUG)
bot.delete_webhook()
bot.polling()