from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from botConfiguration import dp, bot 
from handlers.keyboards.clientKB import main_keyboard, movie_kb, afilmKb
from .data_base import postgre_db


class CVLoader(StatesGroup):
    full_name = State()
    resume = State()

# not working
async def cancel_work(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Cancel work')
    await state.finish()

async def starter(message : types.Message):
    await bot.send_message(message.from_user.id, f'Hi, I\'m cinema bot.\nWhat do you want?', reply_markup=main_keyboard)

async def watching_films(message : types.Message):
    await bot.send_message(message.from_user.id, 'Подивитися фільми', reply_markup=movie_kb)

async def going_now_films(message : types.Message):
    await postgre_db.sql_films_read(message)

async def announced_films(message: types.Message):
    photo_url = 'https://vrgsoft.net/wp-content/uploads/2020/08/logo_shadow.jpg'
    await bot.send_photo(message.from_user.id, photo=photo_url, reply_markup=afilmKb)

async def go_to_mainMenu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Головне меню', reply_markup=main_keyboard)

async def team_join(message: types.Message):
    
    await CVLoader.full_name.set()
    
    await bot.send_message(message.from_user.id, 'Введіть ваше ФІО')

async def enter_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
    await CVLoader.next()
    await bot.send_message(message.from_user.id, 'Якщо ти вирішив приєднатися до нашої команди, то надішли документ у форматі pdf з даними:\nВаше фото, ПІБ, дата народження, досвід роботи та контактний номер телефону')

#! not working yet(i will create db for resume and will be read document and doc id)
async def load_resume(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['resume'] = message.document.file_id
    await postgre_db.add_new_resume_forms(state)
    await bot.send_message(message.from_user.id, 'Ваше резюме надіслано!')
    await state.finish()


def register_handlers_client(dp : Dispatcher):

    dp.register_message_handler(cancel_work, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_work, Text(ignore_case=True, equals='cancel'), state = '*')
    
    dp.register_message_handler(starter, commands=['start'])
    dp.register_message_handler(watching_films, Text(ignore_case=True, equals='Подивитися фільми'))
    dp.register_message_handler(going_now_films, Text(ignore_case=True, equals='Фільми які йдуть зараз'))
    dp.register_message_handler(announced_films, Text(ignore_case=True, equals='Анонси фільмів'))
    
    dp.register_message_handler(team_join, Text(ignore_case=True, equals='Приєднатися до команди'), state=None)
    dp.register_message_handler(enter_full_name, state=CVLoader.full_name)
    dp.register_message_handler(load_resume, content_types=['document'], state=CVLoader.resume)
    
    dp.register_message_handler(go_to_mainMenu, Text(ignore_case=True, equals='В головне меню'))
    
