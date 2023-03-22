import telebot
import requests
from bs4 import BeautifulSoup
import re
import time
from cookie import TOKEN_ID, CHAT_ID, OWNER_ID


TOKEN = TOKEN_ID  # Вставьте свой токен

ALLOWED_USERS = CHAT_ID # Вставьте список разрешенных пользователей

bot = telebot.TeleBot(TOKEN)

for user in ALLOWED_USERS:
    for user in ALLOWED_USERS:
        bot.send_message(int(user), "The bot is working!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я телеграм-бот для работы с ценами в игре Team Fortress 2. Для запуска парсинга используйте команду /start_parsing")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я могу помочь вам узнать текущую стоимость ключей в игре Team Fortress 2.")

@bot.message_handler(commands=['check_prices'])
def send_prices(message):
    if str(message.chat.id) not in ALLOWED_USERS:
        bot.reply_to(message, "У вас нет доступа к этой команде.")
        return

    try:
        url_tf2lavka = 'https://tf2lavka.ru/'
        response = requests.get(url_tf2lavka)
        soup = BeautifulSoup(response.text, 'lxml')
        tf2_key_lavka = soup.find(class_="one-server").find("p").get_text()
        tf2_key_lavka_clean = re.sub('[^0-9\.]', '', tf2_key_lavka)
        tf2_key_lavka_float = float(tf2_key_lavka_clean)

        exchange_url = 'https://steamcommunity.com/market/priceoverview/?appid=440&country=russia&currency=5&market_hash_name=Mann+Co.+Supply+Crate+Key'
        exchange_response = requests.get(exchange_url)
        exchange_data = exchange_response.json()
        tf2_key_steam_string = re.sub('[^0-9\.]','',exchange_data["lowest_price"][:6].replace(',', '.'))
        tf2_key_steam_float = round(float(tf2_key_steam_string) * 0.868,2)
        difference_value = round(tf2_key_steam_float - tf2_key_lavka_float,1)
        if difference_value > 0:
            bot.send_message(message.chat.id, f"Текущая стоимость ключей в TF2 Lavka: {tf2_key_lavka_float} руб.\nТекущая стоимость ключей на Steam: {tf2_key_steam_float} руб.\nТекущая разница: `+{difference_value}`", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"Текущая стоимость ключей в TF2 Lavka: {tf2_key_lavka_float} руб.\nТекущая стоимость ключей на Steam: {tf2_key_steam_float} руб.\nТекущая разница: {difference_value}", parse_mode='Markdown')
    except Exception as e:
        print(e)

@bot.message_handler(commands=['start_parsing'])
def start_parsing(message):
    if str(message.chat.id) not in ALLOWED_USERS:
        bot.reply_to(message, "У вас нет доступа к этой команде.")
        return

    bot.reply_to(message, "Запуск парсинга...")
    while True:
        send_prices(message)
        time.sleep(3600)  # Повторяем запрос каждый час

bot.polling()





