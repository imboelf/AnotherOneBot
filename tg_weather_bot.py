import requests
import datetime

from config import wbot_token, weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token = wbot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет, напиши мне свой город и узнаешь погоду")

@dp.message_handler()
async def get_weather(message: types.Message):
        codemoji = {
            'Clear': "Ясно \U00002600",
            'Clouds': "Облачно \U00002601",
            'Rain': "Дождливо \U00002614",
            'Drizzle': 'Легкий дождик \U00002614',
            'Thunderstorm': 'Гроза \U000026A1',
            'Snow': "Снег \U0001F328",
            "Mist": "Туманно \U0001F32B"
        }
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
            )
            data = r.json()

            city = data['name']
            curr_tmp = data['main']['temp']

            weather_description = data["weather"][0]["main"]
            if weather_description in codemoji:
                wd = codemoji[weather_description]
            else:
                wd = "Чекай сам, че тама творится на улице"

            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            sunrise_timeset = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset_timeset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                  f"Погода в городе: {city}\n"
                  f"Текущая температура: {curr_tmp} C° {wd}\n"
                  f"Давление: {pressure} мм рт. ст.\n"
                  f"Скорость ветра: {wind} м/с\n"
                  f"Рассвет: {sunrise_timeset}\n"
                  f"Закат: {sunset_timeset}\n"
                  f"Хорошего дня!")
        except:
            await message.reply('Ошибка в названии города')

if __name__ == '__main__':
    executor.start_polling(dp)