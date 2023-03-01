import json
import re
import telegram
import asyncio
import requests
from bs4 import BeautifulSoup

bot = telegram.Bot(token='TOKEN_ID')
chat_ids = ['CHAT_ID', 'CHAT_ID']

async def send_prices():
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
    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=f"{tf2_key_steam_float} steam\n{tf2_key_lavka_float} tf2lavka")
    


async def main():
    while True:
        await send_prices()
        await asyncio.sleep(3600)  # Wait for 1 hour


if __name__ == '__main__':
    asyncio.run(main())




