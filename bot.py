import time
import logging
from constants import *
from google_translate_ru_kk import google_translate_ru_kk

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# START


@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(
        f'user_id={user_id} user_full_name={user_full_name} time={time.asctime()}')
    await message.reply(f"Салем, {user_full_name}!\n{greeting}")

    await bot.send_message(user_id, f'Қалдарыңыз қалай, {user_full_name}?')

# MENU


@dp.message_handler(commands=['menu'])
async def show_menu(message: Message):
    # Create the menu

    # buttons for menu
    button_translate_book = InlineKeyboardButton(
        "Библиотека книг", callback_data="button_translate_book")
    button_dictionary = InlineKeyboardButton(
        "Словарь", callback_data="button_dictionary")
    button_translate = InlineKeyboardButton(
        "Переводчик", callback_data="button_translate")
    button_reading = InlineKeyboardButton(
        "Чтение", callback_data="button_reading")
    button_listening = InlineKeyboardButton(
        "Аудио", callback_data="button_listening")
    button_user_translator = InlineKeyboardButton(
        "Я готов переводить", callback_data="button_user_translator")

    # Create the menu
    menu = InlineKeyboardMarkup(row_width=4)
    menu.add(button_translate_book)
    menu.add(button_dictionary, button_translate)
    menu.add(button_reading, button_listening)
    menu.add(button_user_translator)

    # Send the message with the menu
    await message.answer(menu_text, reply_markup=menu)

# BUTTON_TRANSLATE


@dp.callback_query_handler(lambda c: c.data == 'button_translate')
async def process_translate(callback_query: CallbackQuery, state: FSMContext):
    # Set the state to waiting_for_text
    await state.set_state("waiting_for_text")
    # Ask the user to enter a text
    await bot.send_message(callback_query.from_user.id, "Введите слово или текст на русском для перевода на казахский язык")


@dp.message_handler(state="waiting_for_text")
async def translate(message: Message, state: FSMContext):
    # Get the text entered by the user
    text = message.text
    info_text = " ".join(text.split()[:10]) + " ..."
    await bot.send_message(message.from_user.id, f"Переводим: {info_text}.\n Подождите чуть-чуть...")

    # Process the text with google_translate_ru_kk
    result = google_translate_ru_kk(text)

    # Send the result to the user
    await bot.send_message(message.from_user.id, f"Перевод: {result}")

    # Reset the state
    await state.finish()

# start the bot
if __name__ == '__main__':
    executor.start_polling(dp)
