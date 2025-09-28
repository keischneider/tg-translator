import os
import telebot
from dotenv import load_dotenv
from gtts import gTTS
from langdetect import detect, detect_langs
from llm import request
from prompts import raw_dev_prompt, raw_user_prompt
import re

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode='MARKDOWN')
mp3_path = os.getenv('MP3_PATH')

def match_target_language(source_lang):
    match source_lang:
        case 'en':
            return 'de'
        case 'de':
            return 'en'
        case 'ru':
            return 'sk'
        case 'sk':
            return 'ru'
        case _:
            return 'en'


def extract_prefix_symbols(text):
    match = re.match(r'^([^a-zA-Z0-9]*)', text)
    if match:
        symbols = match.group(1)
        remaining_text = text[len(symbols):].strip()
        return (symbols, remaining_text)
    return ('', text)


def parse_symbols(commands, text):
    language = detect(text)
    if '@' in commands:
        language = 'de'
    action = os.getenv('ACTION_TRANSLATE')
    if '!' in commands:
        action = os.getenv('ACTION_CORRECT')
    if '?' in commands:
        action = os.getenv('ACTION_EXPLAIN')
    return {'language': language, 'action': action, 'tts': '*' in commands}


@bot.message_handler()
def command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    commands, text = extract_prefix_symbols(message.text)
    parsed = parse_symbols(commands, text)
    if parsed['tts']:
        bot.send_chat_action(message.chat.id, 'record_audio')
        tts = gTTS(text=text, lang=parsed['language'], slow=False)
        tts.save(mp3_path)
        bot.send_voice(message.chat.id, open(mp3_path, 'rb'))
    target_language = match_target_language(text)
    dev_prompt = raw_dev_prompt.format(from_lang=parsed['language'], to_lang=target_language)
    user_prompt = raw_user_prompt.format(action=parsed['action'], from_lang=parsed['language'], text=text)
    bot.send_chat_action(message.chat.id, 'typing')
    response = request(dev_prompt, user_prompt)
    bot.reply_to(message, response)


print("bot is running...")
bot.infinity_polling()