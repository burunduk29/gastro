import telebot
from telebot import types

TOKEN = '7875106040:AAGitVFyuVJ6Nae_hYyJ_UNIarmCFAfXF94'
bot = telebot.TeleBot(TOKEN)

tours = {
    '1': {
        'name': 'Гастротур-выходного дня',
        'description': 'блаблабла',
        'price': '1000 EUR',
        'dates': '01.07.2024 - 07.07.2024'
    },
    '2': {
        'name': 'Гастротур',
        'description': 'звазаза',
        'price': '800 EUR',
        'dates': '15.07.2024 - 20.07.2024'
    }
}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Показать туры')
    btn2 = types.KeyboardButton('Забронировать тур')
    btn3 = types.KeyboardButton('Контакты')  # Добавляем новую кнопку
    markup.add(btn1, btn2, btn3)  # Добавляем кнопку в разметку

    bot.send_message(message.chat.id,
                     "Привет! Я бот туристического агентства.\nЧем могу помочь?",
                     reply_markup=markup)


# Добавляем новый обработчик для кнопки "Контакты"
@bot.message_handler(func=lambda message: message.text == 'Контакты')
def contacts(message):
    contact_text = "📍 Наш адрес: г. Москва, ул. Примерная, д. 1\n"
    contact_text += "📞 Телефон: +7 (999) 123-45-67\n"
    contact_text += "📧 Email: example@tourism.com\n"
    contact_text += "⏰ Время работы: Пн-Пт 9:00-18:00"

    bot.send_message(message.chat.id, contact_text)


# Остальные обработчики остаются без изменений
@bot.message_handler(func=lambda message: message.text == 'Показать туры')
def show_tours(message):
    for tour_id, tour_info in tours.items():
        tour_text = f"🏷 {tour_info['name']}\n"
        tour_text += f"📝 {tour_info['description']}\n"
        tour_text += f"💰 Цена: {tour_info['price']}\n"
        tour_text += f"📅 Даты: {tour_info['dates']}\n"

        markup = types.InlineKeyboardMarkup()
        book_button = types.InlineKeyboardButton(
            text="Забронировать",
            callback_data=f"book_{tour_id}"
        )
        markup.add(book_button)

        bot.send_message(message.chat.id, tour_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('book_'))
def book_tour(call):
    tour_id = call.data.split('_')[1]
    tour = tours[tour_id]

    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        f"Вы выбрали тур: {tour['name']}\n"
        "Для оформления бронирования, пожалуйста, свяжитесь с нашим менеджером по телефону +7-XXX-XXX-XXXX"
    )


@bot.message_handler(func=lambda message: message.text == 'Забронировать тур')
def book_tour_button(message):
    bot.send_message(
        message.chat.id,
        "Для бронирования выберите интересующий тур в списке туров и нажмите кнопку 'Забронировать'"
    )


if __name__ == "__main__":
    bot.polling(none_stop=True)
