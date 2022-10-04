from glob import glob
import os
from random import choice
from utils import get_smile, main_keyboard, play_random_numbers, has_object_on_image

def greet_user(update, context):
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй, пользователь {context.user_data['emoji']}!",
        reply_markup = main_keyboard(),
        )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    update.message.reply_text(f"{text} {context.user_data['emoji']}",
                                reply_markup = main_keyboard(),
                                )

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup = main_keyboard())

def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id #берем id чата с текущим пользователем
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'), reply_markup = main_keyboard())

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )

def check_user_photo(update, context):
    update.message.reply_text('Обработка фотографии')
    os.makedirs('downloads', exist_ok=True)#exist_ok не перезатирает папку
    photo_file = context.bot.getFile(update.message.photo[-1].file_id) #получаем файл
    file_name = os.path.join('downloads',f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Файл сохранен')
    if has_object_on_image(file_name, 'cat'):
        update.message.reply_text('Обнаружен котик, добавляю в библиотеку.')
        new_file_name = os.path.join('images',f'cat{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Файл удален, котик не обнаружен!')
