from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core import constants
from core.manager.token_manager import load_token

TOKEN = load_token(constants.TOKEN_PATH)

BOT = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
