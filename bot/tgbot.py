import datetime

import telebot
from telebot import types
bot = telebot.TeleBot('5915561601:AAGYQkRwXRmyNujp8wFlU3luhxYkBVWL0Fg')


'''
ready - active/nonactive
username
choice - driver/passenger
busstation - [1-5]
start time
ratingcar

'''
#keyboardsstart
kbstart = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnstart1 = types.KeyboardButton(text='Изменить категорию')
btnstart2 = types.KeyboardButton(text='Выбрать время и машину')
kbstart.add(btnstart1, btnstart2)

#keyboardstation
kbstat =  types.ReplyKeyboardMarkup(resize_keyboard=True)
btnstat1 = types.KeyboardButton(text='Остановка №1')
btnstat2 = types.KeyboardButton(text='Остановка №2')
btnstat3 = types.KeyboardButton(text='Остановка №3')
btnstat4 = types.KeyboardButton(text='Остановка №4')
btnstat5 = types.KeyboardButton(text='Остановка №5')
kbstat.add(btnstat1,btnstat2,btnstat3,btnstat4,btnstat5)

#keyboardpassenger
kbpass = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnpass1 = types.KeyboardButton("Изменить данные")
btnpass2 = types.KeyboardButton("Найти машину")
kbpass.add(btnpass1,btnpass2)

#keyboarddriver
kbdrive = types.ReplyKeyboardMarkup(resize_keyboard = True)
btndrive1 = types.KeyboardButton("Изменить данные")
btndrive2 = types.KeyboardButton("Найти попутчиков")
kbdrive.add(btndrive1,btndrive2)

#keyboardstop
kbstop = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnstop = types.KeyboardButton("Остановить поиск")
kbstop.add(btnstop)




#dictionary
station = {
    'Остановка №1': 1,
    'Остановка №2': 2,
    'Остановка №3': 3,
    'Остановка №4': 4,
    'Остановка №5': 5
}

#start
@bot.message_handler(commands=['start'])
def start(message):
    d = dict()
    bot.send_message(message.chat.id,message)
    d["login"] = '@' + str(message.chat.username)
    sent = bot.send_message(message.chat.id,'Напишите свое имя и фамилию',reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(sent,review,d)


#create name
def review(message,d:dict):
    d["username"] = message.text
    review2(message,d)

#check who is
def review2(message,d:dict):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Водитель')
    btn2 = types.KeyboardButton(text='Пассажир')
    kb.add(btn1,btn2)
    a=bot.send_message(message.chat.id, "Выберите категорию", reply_markup=kb)
    bot.register_next_step_handler(a,driverorpass,d)

def driverorpass(message,d:dict):
    if message.text == "Водитель":
        d["choice"] = "Driver"
        a = bot.send_message(message.chat.id,'Хорошо,тепрь укажите марку и номер вашей машины. ',reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(a, carnum,d)

    elif message.text == "Пассажир":
        d["choice"] = "Passenger"
        a = bot.send_message(message.chat.id,"Выберите остановку у которой вас забрать.",reply_markup=kbstat)
        bot.register_next_step_handler(a,busstation,d)
def carnum(message,d:dict):
    d["car"] = message.text
    a = bot.send_message(message.chat.id, "Напишите кол-во свободных мест в машине.", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(a,places,d)
def places(message,d:dict):
    d["places"] = int(message.text)
    a = bot.send_message(message.chat.id, "Выберите остановку от которой будете подвзвоить людей.", reply_markup=kbstat)
    bot.register_next_step_handler(a, busstation, d)


def busstation(message,d:dict):
    d["mainstation"] = station[message.text]
    a = bot.send_message(message.chat.id,'Теперь напишите удобное для вас время отправления формата hh:mm', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(a,choosetime,d)
def choosetime(message,d:dict):
    time = message.text.split(':')
    hour = time[0]
    minute = time[1]
    d["starttime"] = datetime.time(hour = int(hour),minute = int(minute))
    if d["choice"] == 'Passenger':
        a = bot.send_message(message.chat.id, f'Имя: {d["username"]}\nКатегория: Пассажир\nВыбранная остановка: Остановка №{d["mainstation"]}\nВремя для выезда: {str(d["starttime"])[:-3]}',reply_markup=kbpass)
        #menupass(a)
    else:
        a = bot.send_message(message.chat.id,f'Имя: {d["username"]}\nКатегория: Водитель, автомобиль: {d["car"]}\nКол-во свободных мест: {d["places"]}\nВыбранная остановка: Остановка №{d["mainstation"]}\nВремя для выезда: {str(d["starttime"])[:-3]}', reply_markup=kbdrive)




#Прием всех текстовых штук
@bot.message_handler()
def menu(message):
    global ready
    global choice
    if message.text == "Изменить данные":
        start(message)
    elif message.text == "Найти машину":
        ready = "active"
        #ебануть запрос
        a = bot.send_message(message.chat.id,'Идет поиск подходящего водителя...',reply_markup=kbstop)
    elif message.text == "Остановить поиск":
        ready = "nonactive"
        if choice == "Passenger":
            a = bot.send_message(message.chat.id, "Поиск прекращен", reply_markup=kbpass)
        else: a = bot.send_message(message.chat.id, "Поиск прекращен", reply_markup=kbdrive)

    elif message.text == "Найти попутчиков":
        ready = "active"
        #ебануть запрос
        a = bot.send_message(message.chat.id,"Идет поиск...",reply_markup=kbstop)


bot.polling(none_stop=True)
