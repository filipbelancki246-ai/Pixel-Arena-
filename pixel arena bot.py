"""
Pixel Arena — Telegram bot that launches the game collection as a Mini App.

НАСТРОЙКА (всё в 2 строки ниже):
  1. Впиши токен от @BotFather в BOT_TOKEN.
  2. Впиши https-ссылку на твой размещённый index.html в WEBAPP_URL.
  3. Запусти файл (кнопка ▶ в PyCharm или `python bot.py`).

Никаких переменных окружения не нужно.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    MenuButtonWebApp,
)

# ====================== НАСТРОЙКИ — ВПИШИ СВОИ ЗНАЧЕНИЯ ======================
BOT_TOKEN = "8845983390:AAHv7dRs4lishos6mNM3N86QwTXRtXM4j2w"
WEBAPP_URL = "https://pixel-arena-beige.vercel.app/"
# ==============================================================================

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pixel-arena-bot")

if BOT_TOKEN == "ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BOTFATHER" or not BOT_TOKEN:
    raise SystemExit(
        "Открой bot.py и впиши свой токен в переменную BOT_TOKEN "
        "(получить его можно у @BotFather в Telegram)."
    )
if WEBAPP_URL == "ВСТАВЬ_СЮДА_HTTPS_ССЫЛКУ_НА_INDEX_HTML" or not WEBAPP_URL.startswith("https://"):
    raise SystemExit(
        "Открой bot.py и впиши в переменную WEBAPP_URL публичную https-ссылку "
        "на webapp/index.html (Telegram требует именно https)."
    )

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def play_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🕹️ Играть в Pixel Arena",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "🛡️ <b>PIXEL ARENA</b>\n\n"
        "Джунгли, рыцарь и куча аркадных игр: змейка, мемори, сапёр, "
        "шахматы, бильярд, крестики-нолики, реверси, 2048, тетрис, "
        "виселица и платформер про рыцаря.\n\n"
        "Жми кнопку ниже, чтобы открыть игру.",
        reply_markup=play_keyboard(),
        parse_mode="HTML",
    )


@dp.message(Command("play"))
async def cmd_play(message: Message) -> None:
    await message.answer("Открываю Pixel Arena:", reply_markup=play_keyboard())


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "/start — открыть игру\n"
        "/play — то же самое\n\n"
        "Твой прогресс и рекорды сохраняются на этом устройстве."
    )


async def setup_menu_button() -> None:
    """Adds a persistent 'Play' button next to the chat's message box."""
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Играть",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )


async def main() -> None:
    await setup_menu_button()
    log.info("Bot started. WebApp url: %s", WEBAPP_URL)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
