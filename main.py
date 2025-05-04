import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import aiohttp
import re
import os
from flask import Flask
import threading
import nest_asyncio

# Telegram Bot Tokeni Environment Variable olaraq alınır
API_TOKEN = os.getenv("API_TOKEN")

# Logger
logging.basicConfig(level=logging.INFO)

# Bot və Dispatcher obyektləri
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Flask server (ping üçün)
app = Flask('')

@app.route('/')
def home():
    return "Bot işləyir ✅"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Replit/Railway üçün uyğunlaşdırma
nest_asyncio.apply()
threading.Thread(target=run_flask).start()

# ssstik.io ilə TikTok video yükləmə
async def download_tiktok(url):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': 'Mozilla/5.0'}
            data = {'id': url, 'locale': 'en', 'tt': '1'}
            async with session.post('https://ssstik.io/abc', data=data, headers=headers) as resp:
                html = await resp.text()
                match = re.search(r'href="(https:\/\/[^"]+\.mp4[^"]*)"', html)
                if match:
                    return match.group(1)
    except Exception as e:
        print("TikTok error:", e)
    return None

# sssinstagram.com ilə Instagram video yükləmə
async def download_instagram(url):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': 'Mozilla/5.0'}
            data = {'url': url}
            async with session.post('https://sssinstagram.com/api/ajaxSearch', data=data, headers=headers) as resp:
                json_data = await resp.json()
                links = re.findall(r'https:\/\/[^"]+\.mp4', str(json_data))
                if links:
                    return links[0]
    except Exception as e:
        print("Instagram error:", e)
    return None

# Start komandası
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Salam! 👋\nSadəcə Instagram və ya TikTok linki göndərin, videonu sizə qaytarım 📥")

# Link mesajlarını idarə et
@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()
    await message.reply("Videonu yükləyirəm...⏳")

    video_url = None

    if 'tiktok.com' in url:
        video_url = await download_tiktok(url)
    elif 'instagram.com' in url:
        video_url = await download_instagram(url)
    else:
        await message.reply("Zəhmət olmasa **Instagram** və ya **TikTok** linki göndərin.")
        return

    if video_url:
        try:
            await message.reply_video(video_url)
        except:
            await message.reply(f"📎 Link:\n{video_url}")
    else:
        await message.reply("Videonu yükləmək mümkün olmadı. Linki yoxlayın və yenidən cəhd edin.")

# Botu işə sal
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
