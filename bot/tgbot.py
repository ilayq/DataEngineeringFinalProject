import datetime

import telebot
from telebot import types
bot = telebot.TeleBot('5915561601:AAGYQkRwXRmyNujp8wFlU3luhxYkBVWL0Fg')

ready = "nonactive"
username =""
choice = ""
mainstation = 0
car = ''
starttime = datetime.time(hour =0,minute = 00)

'''
ready - active/nonactive
username
choice - driver/passenger
busstation - [1-5]
start time
rating
car
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

#kayboardstop
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
    global ready,username,choice,mainstation,car,starttime
    ready = "nonactive"
    username = ""
    choice = ""
    mainstation = 0
    car = ''
    starttime = datetime.time(hour=0, minute=00)
    sent = bot.send_message(message.chat.id,'Напишите свое имя и фамилию',reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(sent,review)


#create name
def review(message):
    global username
    username = message.text
    review2(message)

#check who is
def review2(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Водитель')
    btn2 = types.KeyboardButton(text='Пассажир')
    kb.add(btn1,btn2)
    a=bot.send_message(message.chat.id, "Выберите категорию", reply_markup=kb)
    bot.register_next_step_handler(a,driverorpass)

def driverorpass(message):
    global choice
    if message.text == "Водитель":
        choice = "Driver"
        a = bot.send_message(message.chat.id,'Хорошо,тепрь укажите марку и номер вашей машины. Пример - honda 234',reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(a, carnum)

    elif message.text == "Пассажир":
        choice = "Passenger"
        a = bot.send_message(message.chat.id,"Выберите остановку у которой вас забрать.",reply_markup=kbstat)
        bot.register_next_step_handler(a,busstation)
def carnum(message):
    global car
    car = message.text
    a = bot.send_message(message.chat.id, "Выберите остановку от которой будете подвзвоить людей.", reply_markup=kbstat)
    bot.register_next_step_handler(a,busstation)

def busstation(message):
    global mainstation
    mainstation = station[message.text]
    a = bot.send_message(message.chat.id,'Теперь напишите удобное для вас время отправления формата hh:mm', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(a,choosetime)
def choosetime(message):
    time = message.text.split(':')
    hour = time[0]
    minute = time[1]
    starttime = datetime.time(hour = int(hour),minute = int(minute))
    if choice == 'Passenger':
        a = bot.send_message(message.chat.id, f'Имя: {username}\nКатегория: Пассажир\nВыбранная остановка: Остановка №{mainstation}\nВремя для выезда: {str(starttime)[:-3]}',reply_markup=kbpass)
        #menupass(a)
    else:
        a = bot.send_message(message.chat.id,f'Имя: {username}\nКатегория: Водитель, автомобиль: {car}\nВыбранная остановка: Остановка №{mainstation}\nВремя для выезда: {str(starttime)[:-3]}', reply_markup=kbdrive)


#Выбор водилы

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

































'''
#функция сплита и вывода имени
def printFio():
    @bot.message_handler()
    def FirstAndLastName(message):
        name, lastname = message.text.split(' ')[0], message.text.split(' ')[1]
        bot.send_message(message.chat.id, f'Привет {name} {lastname}', parse_mode='html')
        bot.send_message(message.chat.id,'Выбери кто ты')
        bot.register_next_step_handler_by_chat_id(ChooseWho(), message)

#choose who is
def ChooseWho():
    @bot.message_handler()
    def CW():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        website = types.KeyboardButton('Водила')
        start = types.KeyboardButton('Пасажир')
        markup.add(website, start)
'''


#start








#choose who is are










#button





'''
@bot.message_handler()
def get_user_text(message):
    if message.text == "Hello":
        bot.send_message(message.chat.id, " и тебе привет", parse_mode='html')
    elif message.text =="id":
        bot.send_message(message.chat.id, f"твой id: {message.from_user.id}", parse_mode='html')
    elif message.text == "photo":
        bot.send_photo(message.chat.id, )

    else:
        bot.send_message(message.chat.id, "Я тебя не понял", parse_mode='html')
'''
#button norm
'''
@bot.message_handler(commands=['button'])
def websites(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=1)
    website = types.KeyboardButton('Веб сайт')
    start = types.KeyboardButton('Start')

    markup.add(website,start)
    bot.send_message(message.chat.id,'Cool', reply_markup = markup)
'''

bot.polling(none_stop=True)
