import telebot
import openai
from gtts import gTTS
import os
import sys

TELEGRAM_API_KEY = 'security api key telebot'
OPENAI_API_KEY = 'openai_api_key_security'

openai.api_key = OPENAI_API_KEY
# openai.api_base = "https://api.proxyapi.ru/openai/v1" # эту строку можно упустить тогда базовый openai или укажи путь к иному сайту openai
bot = telebot.TeleBot(TELEGRAM_API_KEY)
chat_histories = {}

@bot.message_handler(commands=['stop'])
def stop():
    sys.exit(0)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_message = message.text
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    chat_histories[chat_id].append({"role": "user", "content": user_message})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=chat_histories[chat_id]
        )
        response_content = response.choices[0].message['content'].strip()
        tts = gTTS(response_content, lang='ru')
        audio_file = f"{chat_id}_response.ogg"
        tts.save(audio_file)
        with open(audio_file, 'rb') as audio:
            bot.send_voice(chat_id, audio)
        os.remove(audio_file)
        chat_histories[chat_id].append({"role": "assistant", "content": response_content})

    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {e}")

if __name__ == "__main__":
    print("Бот запущен. Ожидание сообщений...")
    bot.polling(none_stop=True)
