import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
url = 'https://www.kp.ru/daily/anekdot/'
response = requests.get(url = url)
bs = BeautifulSoup(response.text,'lxml')
list_of_joke = bs.find_all('a',class_='sc-1tputnk-2 bOJkdP')
list_of_joke = [x.text for x in list_of_joke]
list_of_jokes =[]
for i in list_of_joke:
    if 'Анекдоты:' in i:
        i = i.replace('Анекдоты:','')
        list_of_jokes.append(i)

token = '6330000414:AAEUtAGSQlQ5DvHeY7_tHr5KLHenXVowC54'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет! Если хочешь прочитать анекдот, отправь '+'")

@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text =='+':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id, "Отправь '+'")

bot.infinity_polling()