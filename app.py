from openai import OpenAI
import os
import telebot
from dotenv import load_dotenv
from gtts import gTTS
from langdetect import detect, detect_langs


load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode='MARKDOWN')
mp3_path = os.get_env('MP3_PATH')


@bot.message_handler()
def command_help(message):
    language = detect(message.text)
    tts = gTTS(text=message.text, lang=language, slow=False)
    tts.save(mp3_path)
    bot.reply_to(message, message.text)
    bot.send_voice(message.chat.id, open(mp3_path, 'rb'))


print("bot is running...")
bot.infinity_polling()