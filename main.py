import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram import executor
from aiogram import types

api_key = '9d45ca14d664eaa1cf4f20ca48a7499d'

bot = Bot(token='6460684839:AAHps-3sFzzDuDdb4SPiLfdvAjvri83zS7M')
dp = Dispatcher(bot)

async def on_startup(dp):
    print("Bot ishladi")

async def on_shutdown(dp):
    print("Hair")

    await bot.session.close()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Salom men sizga ob-havoni yuborshim uchun /weather deb yozin va shaharni nomini yozin")

@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    if not message.text or len(message.text.split()) < 2:
        await message.reply("iltimos shaharni nomini yozin: /weather Moscow")
        return

    city = ' '.join(message.text.split()[1:])
    weather_info = get_weather(api_key, city)
    await message.reply(weather_info, parse_mode=ParseMode.MARKDOWN)

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp'] - 273.15  # Convert temperature to Celsius
        return f"Weather in {city}: {weather_description}, Temperature: {temperature:.2f}°C"
    else:
        return f"Bu shaharni nomi topilmadi: {city}"


if __name__ == '__main__':

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

