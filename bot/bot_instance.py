from os import getenv
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))