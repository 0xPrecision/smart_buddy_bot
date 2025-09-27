from telebot import TeleBot, apihelper

from config_data.env import TELEGRAM_BOT_TOKEN

apihelper.ENABLE_MIDDLEWARE = True
bot = TeleBot(TELEGRAM_BOT_TOKEN)
