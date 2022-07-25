from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

new_film = KeyboardButton('Додати фільм')
resume_watcher = KeyboardButton('Переглянути резюме')
m_menu = KeyboardButton('В головне меню(вийти з адмінки)')

mainkb_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(new_film).add(resume_watcher).add(m_menu)