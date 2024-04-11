import telebot
from gtts import gTTS
import os
from openai import OpenAI

# Инициализация OpenAI
client = OpenAI(
    api_key="sk-ocZsDK2UM23MfVob1ncrgijjrEytVdeU", #check API key"
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Инициализация бота с использованием API токена
bot = telebot.TeleBot('6930572921:AAGOu5tYTypQX8cwzd5TI6xXXVwzHtpFenQ')

def generate_openai_response(user_input):
    """
    Генерирует ответ на сообщение пользователя с использованием OpenAI.
    """
    # Запрос ответа у модели OpenAI
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": user_input}, {"role": "system", "content": "answer in style of a funny clown"}]  # Добавление предыдущих сообщений пользователя
    )

    response = chat_completion.choices[0].message.content

    return response

@bot.message_handler(func=lambda message: True)
def reply_to_message(message):
    user_input = message.text  # Получаем текст сообщения от пользователя

    if user_input.lower() == 'exit':
        bot.reply_to(message, 'Goodbye!')
        return

    # Генерируем ответ от OpenAI с учетом стиля
    response = generate_openai_response(user_input)

    # Озвучиваем ответ нейросети
    tts = gTTS(text=response, lang='ru')
    tts.save('voice_message.mp3')

    # Отправляем голосовое сообщение пользователю
    voice_message = open('voice_message.mp3', 'rb')
    bot.send_voice(message.chat.id, voice_message)

    # Удаляем голосовое сообщение
    os.remove('voice_message.mp3')

if __name__ == "__main__":
    bot.polling()
