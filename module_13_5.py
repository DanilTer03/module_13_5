from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardButton
import asyncio

api = '...'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button, button2)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью', reply_markup = kb)


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Я бот, помогающий твоему здоровью', reply_markup = kb)


@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст.', reply_markup = kb)
    await UserState.age.set()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer(f'Введите свой рост', reply_markup = kb)
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer(f'Введите свой вес', reply_markup = kb)
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий: {calories}', reply_markup = kb)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)