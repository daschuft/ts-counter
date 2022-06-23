import gspread
import telebot
from datetime import date
import config
import os
from os.path import join, dirname
from dotenv import load_dotenv

def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

bot_token = get_from_env('TELEGRAM_BOT_TOKEN')
googlesheet_id = get_from_env('GOOGLESHEET_ID')
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account()

@bot.message_handler(commands = ['start', 'go'])
def send_welcome(message):
    if str(message.from_user.id) in config.users:
        bot.send_message(message.chat.id, 'Привет! Я буду записывать твои расходы в таблицу.\nВведи категорию и сумму через дефис (например, продукты-1000).')
    else:
        bot.send_message(message.chat.id, 'Извини, тебе нельзя пользоваться этим ботом ;(')

@bot.message_handler(content_types='text')
def get_data(message):
    try:
        today = date.today().strftime('%d.%m.%Y')
        category, price = message.text.lower().split('-', 1)
        if category.isdigit() == True:
            bot.send_message(message.chat.id, 'Категория не может быть числом. Используй буквы и попробуй еще раз.')
        elif (price.strip()).isdigit() == False:
            bot.send_message(message.chat.id, 'Цена должна быть числом. Попробуй еще раз.')
        else:
            text_message = f'На {today} в таблицу расходов добавлена запись: категория "{category}", цена — {price} тенге.'
            bot.send_message(message.chat.id, text_message)
            sh = gc.open_by_key(googlesheet_id)
            sh.sheet1.append_row([today, category, price])
            bot.send_message(message.chat.id, 'Введи категорию и сумму через дефис (например, продукты-1000).')
    except:
        bot.send_message(message.chat.id, 'Ошибка! Неправильный формат данных.\nВведи категорию и сумму через дефис (например, продукты-1000).')

if __name__ == '__main__':
    bot.polling(none_stop=True)