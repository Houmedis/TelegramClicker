import telebot
from telebot import types
import json

bot = telebot.TeleBot('5933413950:AAG3MIVxGBxjwluYqW3uSlfPC4Gg9lQwZRY')


def Get_Data(id_, File_Name):
    with open(File_Name) as read_file:
        Data = json.load(read_file)
        return Data


def Register(id_, Data):
    Data[str(id_)] = {}
    Data[str(id_)]['Numbers'] = 0
    Data[str(id_)]['Updates'] = 1
    Data[str(id_)]['Admin'] = 0
    Data[str(id_)]['Name'] = 'NoName'
    return Data

@bot.message_handler(commands=['start'])
def start(message):
    global Data
    User_id = str(message.from_user.id)
    Data = Get_Data(message.from_user.id, "data_file.json")
    print(Data)
    if User_id not in Data:
        Register(User_id, Data)
    Button_list = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Пойти на завод!')
    if Data[User_id]['Admin'] == 1:
        btn2 = types.KeyboardButton('Admin panel')
        Button_list.add(btn1, btn2)
    else:
        Button_list.add(btn1)
    bot.send_message(message.chat.id,
                     text='Здарова, товарищ. Ты пользуешься телеграмм-ботом ЛиКойник, пока он работает на благо партии.',
                     reply_markup=Button_list)
    
    
@bot.message_handler(content_types=['text'])
def Coins(message):
    global Data
    User_id = str(message.from_user.id)
    if User_id not in Data:
        Data = Register(User_id, Data)
    if message.text == 'Слава пролетариату!':
        Data[User_id]['Numbers'] += Data[User_id]['Updates']

    elif message.text == 'Узнать количество SocialCredit':
        bot.send_message(message.chat.id,
                         text=f'Товарищ, у вас {Data[User_id]["Numbers"]} SocialCredit')
    elif message.text == 'Admin panel' and Data[User_id]['Admin'] == 1:
        Saving = True
        Button_list_Shop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_s = types.KeyboardButton('Сохранить')
        back = types.KeyboardButton('Вернуться на главное меню')
        Button_list_Shop.add(btn1_s, back)
        bot.send_message(message.chat.id,
                         text='Сохранить прогресс?',
                         reply_markup=Button_list_Shop)
    elif message.text == 'Рынок труда':
        Button_list_Shop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_s = types.KeyboardButton('Да')
        back = types.KeyboardButton('Вернуться на завод')
        Button_list_Shop.add(btn1_s, back)
        bot.send_message(message.chat.id,
                         text=f'У тебя {Data[User_id]["Updates"]} бригад. Нанять ещё бригаду за {10 * Data[User_id]["Updates"]} монет?',
                         reply_markup=Button_list_Shop)
        
    elif message.text == 'Да':
        if Data[User_id]['Numbers'] >= 10 * Data[User_id]['Updates']:
            Data[User_id]['Numbers'] -= Data[User_id]['Updates'] * 10
            Data[User_id]['Updates'] += 1
            bot.send_message(message.chat.id,
                             text='Вы успешно наняли одну бригаду')
            
        else:
            bot.send_message(message.chat.id,
                             text='Товарищ, у вас не хватает очков')
            
    elif message.text == 'Пойти на завод!' or message.text == 'Вернуться на завод':
        Button_list = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Слава пролетариату!')
        btn2 = types.KeyboardButton('Узнать количество SocialCredit')
        btn3 = types.KeyboardButton('Рынок труда')
        Button_list.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Здарова, товарищ. Ты должен гордиться тем, что трудишься на Родину.',
                         reply_markup=Button_list)
        
    else:
        bot.send_message(message.chat.id,
                         text='Товарищ, не страдайте бездельем, выполняйте квоту')
bot.polling()