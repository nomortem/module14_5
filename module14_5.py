from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from crud_function import add_user, is_included, initiate_db

# Инициализация бота
bot = Bot(token='7545702137:AAFmT_fwP09R5q35yTR0VgMvrL55nQMYKCQ')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация состояний
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.reply("Добро пожаловать! Для регистрация используйте команду Регистрация")

@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.reply("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.reply("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.reply("Пользователь существует, введите другое имя.")

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.reply("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    age = message.text

    add_user(username, email, age)
    await message.reply("Вы успешно зарегистрированы!")
    await state.finish()

# Запуск бота
if __name__ == '__main__':
    import asyncio
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)