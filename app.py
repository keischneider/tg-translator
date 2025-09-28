import os
import telebot
from dotenv import load_dotenv
from gtts import gTTS
from langdetect import detect, detect_langs
from llm import request
from prompts import dev_prompt_de, dev_prompt_en, raw_user_prompt

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode='MARKDOWN')
mp3_path = os.getenv('MP3_PATH')


@bot.message_handler()
def command_help(message):
    language = detect(message.text)
    text = message.text
    action = os.getenv('ACTION_TRANSLATE')
    if text[0] == '!':
        action = os.getenv('ACTION_CORRECT')
        text = text[1:].strip()
    elif text[0] == '?':
        action = os.getenv('ACTION_EXPLAIN')
        text = text[1:].strip()
    user_prompt = raw_user_prompt.format(action=action, text=text)
    response = os.getenv('DEFAULT_RESPONSE')
    if language == 'de':
        response = request(dev_prompt_de, user_prompt)
    elif language == 'en':
        response = request(dev_prompt_en, user_prompt)
    if action == os.getenv('ACTION_TRANSLATE'):
        tts = gTTS(text=response, lang=detect(response), slow=False)
        tts.save(mp3_path)
        bot.send_voice(message.chat.id, open(mp3_path, 'rb'))
    bot.reply_to(message, response)


print("bot is running...")
bot.infinity_polling()