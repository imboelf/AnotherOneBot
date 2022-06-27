import requests
import datetime
from pprint import pprint
from config import weather_token

def get_weather(city, weather_token):
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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

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

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n***"
              f"Погода в городе: {city}\n"
              f"Текущая температура: {curr_tmp} C° {wd}\n"
              f"Давление: {pressure} мм рт. ст.\n"
              f"Скорость ветра: {wind} м/с\n"
              f"Рассвет: {sunrise_timeset}\n"
              f"Закат: {sunset_timeset}\n"
              f"Хорошего дня!")
    except Exception as ex:
        print(ex)
        print('Ошибка в названии города')

def main():
    city = input('Введите запрос: ')
    get_weather(city, weather_token)


if __name__ == '__main__':
    main()