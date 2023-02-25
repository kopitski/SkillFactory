import telebot

from extensions import Converter, APIException
from config import currency, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def start(message: telebot.types.Message):
    text = "Приветствие!\n" \
           "Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты>\
           <в какую валюту перевести> <количество>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for i in currency.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
        """base - from which currency are we converting from (из какой валюты конвертируем) / 
            sym - to which currency are we converting to (в какую валюту конвертируем) """
    except ValueError as e:
        bot.reply_to(message, "Неверное количество параметров")

    try:
        total = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f'Цена {amount} {base} в {sym}: {total} ')
    except APIException as e:
        bot.reply_to(message, f'Неверно ввели параметр:\n{e}')


bot.polling()