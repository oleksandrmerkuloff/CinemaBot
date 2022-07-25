from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from botConfiguration import bot, dp
from .keyboards import adminKb, clientKB
from .data_base import postgre_db

_ADMIN_PASS = 'your admin password' #you can create db with passwords

class Admin(StatesGroup):
    try_pass = State()

class NewFilm(StatesGroup):
    poster_img = State()
    film_title = State()
    genre = State()
    age_limit = State()
    description = State()
    film_url = State()

async def cancel_work(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Cancel work')
    await state.finish()


async def admin_check(message: types.Message):
    await Admin.try_pass.set()
    await message.reply('Enter admin password')

async def enter_pass(message: types.Message, state: FSMContext):
    if message.text.lower() == _ADMIN_PASS:
        async with state.proxy() as data:
            data['try_pass'] = message.text
        await bot.send_message(message.from_user.id, 'Перевірка пройдена!', reply_markup=adminKb.mainkb_admin)
        await message.delete()
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Спробуйте ще раз! Або введіть "cancel"')

async def watcher_resume(message: types.Message):
    await postgre_db.sql_resume_read(message)

# Робота з меню адміна 
async def add_film(message: types.Message):
    await NewFilm.poster_img.set()
    await bot.send_message(message.from_user.id, 'Завантажте постер фільму') 

async def load_poster(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        data['poster_img'] = message.photo[0].file_id
    await NewFilm.next()
    await bot.send_message(message.from_user.id, 'Введіть назву фільму')     

async def entering_filmTitle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['film_title'] = message.text
    await NewFilm.next()
    await bot.send_message(message.from_user.id, 'Введіть жанр фільму')

async def entering_genre(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['genre'] = message.text
    await NewFilm.next()
    await bot.send_message(message.from_user.id, 'Введіть вікові обмеження(exemp: "18+")')

async def entering_age_limit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age_limit'] = message.text
    await NewFilm.next()
    await bot.send_message(message.from_user.id, 'Введіть короткий опис фільму')

async def entering_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await NewFilm.next()
    await bot.send_message(message.from_user.id, 'Посилання на сторінку фільму')

async def entering_film_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['film_url'] = message.text
    
    await postgre_db.add_new_film_in_table(state)
    await bot.send_message(message.from_user.id, 'Новий фільму було додано')
    await state.finish()


async def admin_exit(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вихід...', reply_markup=clientKB.main_keyboard)


def register_handlers_admin(dp : Dispatcher):
    
    dp.register_message_handler(cancel_work, commands=['cancel'], state='*')
    dp.register_message_handler(cancel_work, Text(equals='cancel', ignore_case = True), state="*")

    dp.register_message_handler(admin_check, commands=['admin'], state=None)
    dp.register_message_handler(enter_pass, state=Admin.try_pass)

    #additional new film
    dp.register_message_handler(add_film, Text(ignore_case=True, equals='Додати фільм'), state= None)
    dp.register_message_handler(load_poster, content_types=['photo'], state= NewFilm.poster_img)
    dp.register_message_handler(entering_filmTitle, state= NewFilm.film_title)
    dp.register_message_handler(entering_genre, state= NewFilm.genre)
    dp.register_message_handler(entering_age_limit, state= NewFilm.age_limit)
    dp.register_message_handler(entering_description, state= NewFilm.description)
    dp.register_message_handler(entering_film_url, state= NewFilm.film_url)
    
    dp.register_message_handler(watcher_resume, Text(ignore_case=True, equals='Переглянути резюме'))

    dp.register_message_handler(admin_exit, Text(ignore_case=True, equals='В головне меню(вийти з адмінки)'))