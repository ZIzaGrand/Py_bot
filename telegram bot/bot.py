import bot_setup

import logging


import sqlite3
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# poken = token.token

bot = Bot(token=bot_setup.TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



class Form(StatesGroup):
    heabline = State()
    description = State()


@dp.message_handler(commands='rec')
async def cmd_start(message: types.Message):

    await Form.heabline.set()

    await message.reply("Напишите заголовок")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.heabline)
async def process_heabline(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['heabline'] = message.text

    await Form.next()
    await message.reply("Напишите описание")




@dp.message_handler(state=Form.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

        conn = sqlite3.connect('TGP.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(heabline TEXT, description TEXT)')
        cur.execute(f'INSERT INTO users VALUES("{ data["heabline"]}","{ data["description"]}")')
        for i in cur.execute("SELECT * FROM users"):
        	print(i)
        conn.commit()
        conn.close()
        await message.reply("Данные записались")
    await state.finish()




class Find(StatesGroup):
    heabline = State()
    description = State()


@dp.message_handler(commands=['find'])
async def find_heabline(message: types.Message):

    await Find.heabline.set()
    await message.reply("Что хотите найти?")


@dp.message_handler(state=Find.heabline)
async def write_heabline(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['heabline'] = message.text

        conn = sqlite3.connect('TGP.db')
        cur = conn.cursor()
        finde = (f"SELECT description FROM users WHERE heabline = ?")
        cur.execute(finde, (data['heabline'],))
        deck = cur.fetchone()

        await message.reply(deck[0])



    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


