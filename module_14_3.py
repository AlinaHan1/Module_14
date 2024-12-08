from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb_gender = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мужской'),
         KeyboardButton(text='Женский')]
    ], resize_keyboard=True
)

kb_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формула расчета', callback_data='formulas'),
         InlineKeyboardButton(text='Информация', callback_data='info')],
        [InlineKeyboardButton(text='Купить', callback_data='buy')]
    ], resize_keyboard=True
)

kb_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт №1 ', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт №2 ', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт №3 ', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт №4 ', callback_data='product_buying')]
    ], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью', reply_markup=kb_start)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.callback_query_handler(text='formulas')
async def info_gender(call):
    await call.message.answer('Укажите свой пол:', reply_markup=kb_gender)
    await call.answer()


@dp.message_handler(text=['Мужской', 'Женский'])
async def set_gender(message):
    if message.text == 'Мужской':
        await message.answer(f'10 x вес(кг) + 6,25 х рост(см) - 5 х возраст(лет) + 5')
    if message.text == 'Женский':
        await message.answer(f'10 x вес(кг) + 6,25 х рост(см) - 5 х возраст(лет) - 161')


@dp.callback_query_handler(text='buy')
async def get_buying_list(call):
    with open('files/5.jpg', 'rb') as img:
        await call.message.answer('Название: Продукт "Капибарка" | Описание: милашка | Цена: 100 обнимашек')
        await call.message.answer_photo(img)
    with open('files/4.png', 'rb') as img:
        await call.message.answer('Название: Продукт "Две капибарки" | Описание: милота в квадрате'
                                  '| Цена: 200 поцелуйчиков')
        await call.message.answer_photo(img)
    with open('files/2.jpg', 'rb') as img:
        await call.message.answer('Название: Продукт "Тазик капибарок" | Описание: Донт Вори, би каппи '
                                  '| Цена: 300 комплементов')
        await call.message.answer_photo(img)
    with open('files/3.png', 'rb') as img:
        await call.message.answer('Название: Продукт "Много капибарок не бывает" '
                                  '| Описание: Сама не знаю что с этим делать | Цена: 400 лучиков любви')
        await call.message.answer_photo(img)
    await call.message.answer('Выберете продукт для покупки: ', reply_markup=kb_product)
    await call.answer()


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Поздравляем! Вы успешно приобрели продукт!')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Укажите свой пол:', reply_markup=kb_gender)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    await state.update_data(gender=message.text)
    if UserState.gender == 'men':
        data = await state.get_data()
        norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        await message.answer(f'Ваша норма калорий: {norm} ') # reply_markup=types.ReplyKeyboardRemove()
    else:
        data = await state.get_data()
        norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer(f'Ваша норма калорий: {norm} ')
    await state.finish()


@dp.callback_query_handler(text='info')
async def all_message(call):
    await call.message.answer('Я бот, помогающий рассчитать дневную норму калорий.')
    await call.answer()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, что бы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
