from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.dispatcher import FSMContext
# import asyncio
from crud_functions_14_5 import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

get_all_products()

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
request_botton = KeyboardButton(text='Рассчитать')
inform_botton = KeyboardButton(text='Информация')
buy_botton = KeyboardButton(text='Купить')
registration_botton = KeyboardButton(text='Регистрация')
start_kb.row(request_botton, inform_botton)
start_kb.row(buy_botton)
start_kb.row(registration_botton)

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
request_in_botton = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='Calories')
inform_in_botton = InlineKeyboardButton(text='Формула для расчёта', callback_data='Formula')
kb_in.row(request_in_botton, inform_in_botton)

kb_products = InlineKeyboardMarkup(resize_keyboard=True)
product_buttons = []
for product in get_all_products():
    product_buttons.append(InlineKeyboardButton(text=f'{product[1]}', callback_data="product_buying"))
for i in range(0, len(product_buttons), 2):
    kb_products.row(product_buttons[i], product_buttons[i + 1])


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State('1000')


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите операцию', reply_markup=kb_in)


@dp.callback_query_handler(text='Formula')
async def get_formula(call):
    await call.message.answer('Формула для расчёта оптимального количества получаемых килокалорий (кК): '
                              'Норма кК = 1,2 * [10 * вес(в кг) + 6,25 * рост(в см) - 5 * возраст(в годах) + 5].')
    await call.answer()


@dp.callback_query_handler(text='Calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст в годах: целое число от 13 до 80.')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост в сантиметрах.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свою массу в килограммах.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    quantity_kilocalories = 1.2 * (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']))
    await message.answer(f'Для сохранения нормального веса или для оптимального похудения при средней физической '
                         f'активности Вам необходимо получать {quantity_kilocalories} килокалорий в сутки.')
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите Ваше имя (использовать только латинский алфавит).')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Такой пользователь существует, введите другое имя.')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email.')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст в годах.')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    try:
        if 0 <= int(message.text) <= 150:
            await state.update_data(age=message.text)
            new_user_data = await state.get_data()
            add_user(new_user_data['username'], new_user_data['email'], new_user_data['age'])
            await message.answer('Регистрация прошла успешно.')
            await state.finish()
        else:
            await message.answer('Возраст введён неверно, введите возраст правильно.')
    except ValueError:
        await message.answer('Возраст введён некорректно, введите целое число лет.')


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for number, product in enumerate(get_all_products()):
        await message.answer(f'Название: {product[1]} | '
                             f'Описание: {product[2]} '
                             f'| Цена: {product[3]}')
        with open(f'flower{number + 1}.jpg', "rb") as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_products)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_messages(message):
    await message.answer('Привет! Я бот, помогающий Вашему здоровью. \nЕсли хотите узнать количество килокалорий, '
                         'которое нужно получать Вам для сохранения нормального веса или для оптимального похудения, '
                         'нажмите на кнопку "Рассчитать". '
                         '\nЕсли хотите узнать формулу для расчёта, нажмите кнопку "Формула для расчёта". '
                         '\nЕсли хотите купить продукт, нажмите кнопку "Купить". '
                         '\nЕсли хотите получать актуальную информацию о продуктах и о текущих акциях,'
                         'пройдите регистрацию (для этого нажмите кнопку "Регистрация").', reply_markup=start_kb)


@dp.message_handler(text=['Спасибо.', 'Спасибо', 'спасибо', 'Спасибо!'])
async def set_age(message):
    await message.answer('Пожалуйста!')
    await UserState.age.set()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
