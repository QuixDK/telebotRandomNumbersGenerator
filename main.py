import telebot
import random

bot = telebot.TeleBot('YOUR-TOKEN-HERE')

@bot.message_handler(commands=['start'])
def generate_message(message):
    admins = bot.get_chat_administrators(message.chat.id)
    admin_ids = [admin.user.id for admin in admins]
    if message.from_user.id in admin_ids:
        bot.send_message(message.chat.id, 'Генератор случайных чисел приветствует вас! \nВведите числовой диапазон, количество чисел и нужно ли генерировать повторяющиеся числа в формате: "от до количество да/нет", например: "1 100 10 да".')
        bot.register_next_step_handler(message, generate_numbers)
    else:
        bot.register_next_step_handler(message, generate_numbers)

def generate_numbers(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]
        if message.from_user.id in admin_ids:
            min_value, max_value, count, with_repeats = message.text.split()
            min_value, max_value, count = int(min_value), int(max_value), int(count)
            with_repeats = with_repeats.lower() == 'да'
            if with_repeats:
                numbers = [random.randint(min_value, max_value) for i in range(count)]
            else:
                numbers = random.sample(range(min_value, max_value + 1), count)
            result = []
            for num in numbers:
                result.append(f'{num} ✅')
            nl_char = '\n'
            bot.send_message(message.chat.id, f'Результат получен:\n{nl_char.join(result)}')
        else:
            bot.register_next_step_handler(message, generate_numbers)
    except:
        bot.send_message(message.chat.id, 'Ошибка! Неверно введены данные, попробуйте еще раз" Пример: "1 100 10 да".')
        bot.register_next_step_handler(message, generate_numbers)

bot.polling(none_stop=True)
