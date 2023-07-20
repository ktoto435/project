import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
url = 'https://www.kfc.ru/coupons'
response = requests.get(url=url)
bs = BeautifulSoup(response.text,'lxml')
coupons = bs.find_all('div',class_='_2NyuN9wIxb _2863BpiS1v')
list_of_coupons =[]
for coupon in coupons:
    try:
        link = 'https://www.kfc.ru' + coupon.find('a', class_='RTQ7M5RnH1').get('href')
        number_of_coupon = coupon.find('div', class_='_2pr76I4WPm').text
        description = coupon.find('div', class_='_3POebZQSBG').text
        old_price = coupon.find('span', class_='fZklbU_aGI condensed').text
        new_price = coupon.find_all('span')[1].text
    except AttributeError:
        link = '-'
        number_of_coupon = '-'
        description = '-'
        old_price = '-'
        new_price = '-'

    pre_list_of_coupons =[number_of_coupon,link,description,old_price,new_price]
    if pre_list_of_coupons[1]!='-':
         list_of_coupons.append(pre_list_of_coupons)

token = '6329080544:AAFL4DiVEGEk_Zk6S1kX0656v6vfFTCWutU'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('Да!')
    markup.add(bt1)
    bot.send_message(message.chat.id, 'Привет!👋 Хочешь получать свежие купоны KFC?🍔', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_coupons(message):
    if message.text == 'Да!' and list_of_coupons!=[]:
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('Ссылка на сайт',url = list_of_coupons[0][1])
        markup.add(bt1)
        bot.send_message(message.chat.id, f'Номер купона:{list_of_coupons[0][0]}\n Описание:{list_of_coupons[0][2]} \n Старая цена:{list_of_coupons[0][3]} \n Новая цена: {list_of_coupons[0][4]}',reply_markup=markup)
        del list_of_coupons[0]
    elif message.text == 'Да!' and list_of_coupons==[]:
        bot.send_message(message.chat.id,'Купоны закончились')
    else:
        bot.send_message(message.chat.id,'Я ничего не понимаю!')
bot.infinity_polling()