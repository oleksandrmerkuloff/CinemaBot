from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

# Main keyboard
#buy_tickets = KeyboardButton('Придбати квитки') Потім буде так, виводиться інлайн кнопка під кожним фільмом з надписом
# "придбати квитки" яка веде на сторінку фільму на сайті 

films = KeyboardButton('Подивитися фільми')
work_offer = KeyboardButton('Приєднатися до команди')

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(films).add(work_offer)

# Keyboard if you looking for a film
going_film = KeyboardButton('Фільми які йдуть зараз')
future_films = KeyboardButton('Анонси фільмів')
m_menu = KeyboardButton('В головне меню')

movie_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(going_film).add(future_films).add(m_menu)

# inline button for announced_films
afilm_btn = InlineKeyboardButton(text='Переглянути майбутні фільми', url='https://multiplex.ua/ru/soon')

afilmKb = InlineKeyboardMarkup().add(afilm_btn)

# inline button for going_films
def createKb(link):
    buy_tickets_btn = InlineKeyboardButton(text='Придбати квитки на фільм', url=str(link))

    tickets_buy_kb = InlineKeyboardMarkup().add(buy_tickets_btn)

    return tickets_buy_kb