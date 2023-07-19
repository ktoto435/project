import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
url = 'https://www.kp.ru/daily/anekdot/'
response = requests.get(url=url)
bs = BeautifulSoup(response.text,'lxml')
pre_jokes = bs.find_all('a',class_='sc-1tputnk-2 bOJkdP')
jokes = [i.text.replace('Анекдоты:','') for i in pre_jokes]
list_of_jokes = [i[1:] for i in jokes]


token='6360480229:AAFhr9u90TgC8UtWJbtSf05iTGLYFCDQddE'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!👋')
    markup = types.ReplyKeyboardMarkup()
    bt1= types.KeyboardButton('Анекдоты')
    bt2 = types.KeyboardButton('Евгений Пригожин')
    markup.add(bt1,bt2)
    bot.send_message(message.chat.id, 'Что ты хочешь от меня услышать?', reply_markup= markup)


@bot.message_handler(content_types=['text'])
def reply(message):
    if message.text =='Анекдоты':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    elif message.text =='Евгений Пригожин':
        photo2 = open('Пригожин2.png', 'rb')
        bot.send_photo(message.chat.id, photo2)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


bot.infinity_polling()


