from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler, CallbackQueryHandler
import telegram
import time
import logging
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors
import io
import re
from matplotlib import rcParams

bot = telegram.Bot(token='5637376738:AAEliHovXHBx6O_0pKcIRePBgEOR8S9N8xU' )
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
PLOT, GENDER, PHOTO, LOCATION, BIO, TRANSIT, SECONDPLOT, PHOTO2, TRANSIT2, PHOTO3, TRANSIT3, FREE_CABS = range(12)

# функция обратного вызова точки входа в разговор
# def start(update, _):
#     update.message.reply_text(
#         'отправь /plot для графика'
#         'отправь гороскоп для гороскопа'
#         'Команда /cancel, чтобы прекратить разговор.\n\n')
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет, это studenthelper. Бот- помощник для студентов муита\n\n"
        "/help - чтобы увидеть доступные команды\n"
        "/plot - чтобы визуализировать возможные исходы оценки за семестр, на основе других оценок\n"
        "/free_cabs - посмотреть свободные кабинеты\n"
        "/how_to_rk1 - обьяснение, как читать график для рк1\n"
        "/how_to_rksrd - обьяснение, как читать график для рксрд\n"
        "/cancel - вернуться в меню\n"
        "Десятичная часть отделяется точкой")
    return ConversationHandler.END
# def start(bot, update):
#     keyboard = [
#                 [InlineKeyboardButton("Click button 1", callback_data='callback_1')],
#                 [InlineKeyboardButton("Click button 1", callback_data='callback_2')]
#             ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     message_reply_text = 'Click one of these buttons'
#     update.message.reply_text(message_reply_text, reply_markup=reply_markup)
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Доступные команды:-\n"
    "/plot - визуализация возможных исходов оценки за семестр(тотал), на основе других оценок\n"
    "/free_cabs - посмотреть свободные кабинеты\n"
    "/how_to_rk1 - обьяснение, как читать график для рк1\n"
    "/how_to_rksrd - обьяснение, как читать график для рксрд\n"
    "/cancel - вернуться в меню\n"
    "Десятичная часть отделяется точкой")
    return ConversationHandler.END
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'действие отменено', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END

def free_cabs(update,context):
    update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def main_menu(update,context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Понедельник', callback_data='m1')],
              [InlineKeyboardButton('Вторник', callback_data='m2')],
              [InlineKeyboardButton('Среда', callback_data='m3')],
              [InlineKeyboardButton('Четверг', callback_data='m4')],
              [InlineKeyboardButton('Пятница', callback_data='m5')],
              [InlineKeyboardButton('Суббота', callback_data='m6')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
    return 'Choose the day of the week:'

def Monday_menu(update,context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                            text=Monday_menu_message(),
                            reply_markup=Monday_menu_keyboard())
                
def Monday_submenu(update,context):
    query = update.callback_query
    query.answer()
    day = update.callback_query.data.split(',')[0]
    time = update.callback_query.data.split(',')[1]
    free_cabs = pd.read_excel(r'C:\Users\Dair\Desktop\magnum\Free Cabinets.xlsx', header = 2)#.pivot(index = 'Time', columns = 'Day', values = 'Cabinet')
    free_cabs['Time'] = free_cabs['Time'].apply(lambda x: '0' + x if len(x) < 18 else x)
    free_cabs['begin'] = free_cabs['Time'].apply(lambda x: x[0:8])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs['end'] = free_cabs['Time'].apply(lambda x: '0' + x[11:19] if len(x) < 19 else x[10:19])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs.columns = free_cabs.columns.str.strip().str.lower()
    cabs_list = free_cabs[(free_cabs['day'] == day)&(free_cabs['time'] == time)]['cabinet'].values
    cabs_list = [x[:5] for x in cabs_list if ('-' not in x)&
                 ('В' not in x)&
                 ('C' not in x)&
                 ('O' not in x)&
                 ('С' not in x)&
                 ('B' not in x)&
                 ('ф' not in x)&
                 ('i' not in x)]
    update.callback_query.message.edit_text(f'{day} \n{time} \n------------\n{", ".join(sorted(cabs_list))}')
def Monday_menu_keyboard():
    keyboard = [[InlineKeyboardButton('8:00:00 - 8:50:00', callback_data='Monday,08:00:00 - 8:50:00')],
                [InlineKeyboardButton('9:00:00 - 9:50:00', callback_data='Monday,09:00:00 - 9:50:00')],
                [InlineKeyboardButton('10:00:00 - 10:50:00', callback_data='Monday,10:00:00 - 10:50:00')],
                [InlineKeyboardButton('11:00:00 - 11:50:00', callback_data='Monday,11:00:00 - 11:50:00')],
                [InlineKeyboardButton('12:10:00 - 13:00:00', callback_data='Monday,12:10:00 - 13:00:00')],
                [InlineKeyboardButton('13:10:00 - 14:00:00', callback_data='Monday,13:10:00 - 14:00:00')],
                [InlineKeyboardButton('14:10:00 - 15:00:00', callback_data='Monday,14:10:00 - 15:00:00')],
                [InlineKeyboardButton('15:10:00 - 16:00:00', callback_data='Monday,15:10:00 - 16:00:00')],
                [InlineKeyboardButton('16:10:00 - 17:00:00', callback_data='Monday,16:10:00 - 17:00:00')],
                [InlineKeyboardButton('17:20:00 - 18:10:00', callback_data='Monday,17:20:00 - 18:10:00')],
                [InlineKeyboardButton('18:30:00 - 19:20:00', callback_data='Monday,18:30:00 - 19:20:00')],
                [InlineKeyboardButton('19:30:00 - 20:20:00', callback_data='Monday,19:30:00 - 20:20:00')],
                [InlineKeyboardButton('20:30:00 - 21:20:00', callback_data='Monday,20:30:00 - 21:20:00')],
                [InlineKeyboardButton('21:30:00 - 22:20:00', callback_data='Monday,21:30:00 - 22:20:00')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def Monday_menu_message():
    return 'Choose time in Monday menu:'
        
def Tuesday_menu(update,context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                            text=Tuesday_menu_message(),
                            reply_markup=Tuesday_menu_keyboard())
                
def Tuesday_submenu(update,context):
    query = update.callback_query
    query.answer()
    day = update.callback_query.data.split(',')[0]
    time = update.callback_query.data.split(',')[1]
    free_cabs = pd.read_excel(r'C:\Users\Dair\Desktop\magnum\Free Cabinets.xlsx', header = 2)#.pivot(index = 'Time', columns = 'Day', values = 'Cabinet')
    free_cabs['Time'] = free_cabs['Time'].apply(lambda x: '0' + x if len(x) < 18 else x)
    free_cabs['begin'] = free_cabs['Time'].apply(lambda x: x[0:8])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs['end'] = free_cabs['Time'].apply(lambda x: '0' + x[11:19] if len(x) < 19 else x[10:19])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs.columns = free_cabs.columns.str.strip().str.lower()
    cabs_list = free_cabs[(free_cabs['day'] == day)&(free_cabs['time'] == time)]['cabinet'].values
    cabs_list = [x[:5] for x in cabs_list if ('-' not in x)&
                 ('В' not in x)&
                 ('C' not in x)&
                 ('O' not in x)&
                 ('С' not in x)&
                 ('B' not in x)&
                 ('ф' not in x)&
                 ('i' not in x)]
    update.callback_query.message.edit_text(f'{day} \n{time} \n------------\n{", ".join(sorted(cabs_list))}')
def Tuesday_menu_keyboard():
    keyboard = [[InlineKeyboardButton('8:00:00 - 8:50:00', callback_data='Tuesday,08:00:00 - 8:50:00')],
                [InlineKeyboardButton('9:00:00 - 9:50:00', callback_data='Tuesday,09:00:00 - 9:50:00')],
                [InlineKeyboardButton('10:00:00 - 10:50:00', callback_data='Tuesday,10:00:00 - 10:50:00')],
                [InlineKeyboardButton('11:00:00 - 11:50:00', callback_data='Tuesday,11:00:00 - 11:50:00')],
                [InlineKeyboardButton('12:10:00 - 13:00:00', callback_data='Tuesday,12:10:00 - 13:00:00')],
                [InlineKeyboardButton('13:10:00 - 14:00:00', callback_data='Tuesday,13:10:00 - 14:00:00')],
                [InlineKeyboardButton('14:10:00 - 15:00:00', callback_data='Tuesday,14:10:00 - 15:00:00')],
                [InlineKeyboardButton('15:10:00 - 16:00:00', callback_data='Tuesday,15:10:00 - 16:00:00')],
                [InlineKeyboardButton('16:10:00 - 17:00:00', callback_data='Tuesday,16:10:00 - 17:00:00')],
                [InlineKeyboardButton('17:20:00 - 18:10:00', callback_data='Tuesday,17:20:00 - 18:10:00')],
                [InlineKeyboardButton('18:30:00 - 19:20:00', callback_data='Tuesday,18:30:00 - 19:20:00')],
                [InlineKeyboardButton('19:30:00 - 20:20:00', callback_data='Tuesday,19:30:00 - 20:20:00')],
                [InlineKeyboardButton('20:30:00 - 21:20:00', callback_data='Tuesday,20:30:00 - 21:20:00')],
                [InlineKeyboardButton('21:30:00 - 22:20:00', callback_data='Tuesday,21:30:00 - 22:20:00')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def Tuesday_menu_message():
    return 'Choose time in Tuesday menu:'
    
def Wednesday_menu(update,context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                            text=Wednesday_menu_message(),
                            reply_markup=Wednesday_menu_keyboard())
                
def Wednesday_submenu(update,context):
    query = update.callback_query
    query.answer()
    day = update.callback_query.data.split(',')[0]
    time = update.callback_query.data.split(',')[1]
    free_cabs = pd.read_excel(r'C:\Users\Dair\Desktop\magnum\Free Cabinets.xlsx', header = 2)#.pivot(index = 'Time', columns = 'Day', values = 'Cabinet')
    free_cabs['Time'] = free_cabs['Time'].apply(lambda x: '0' + x if len(x) < 18 else x)
    free_cabs['begin'] = free_cabs['Time'].apply(lambda x: x[0:8])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs['end'] = free_cabs['Time'].apply(lambda x: '0' + x[11:19] if len(x) < 19 else x[10:19])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs.columns = free_cabs.columns.str.strip().str.lower()
    cabs_list = free_cabs[(free_cabs['day'] == day)&(free_cabs['time'] == time)]['cabinet'].values
    cabs_list = [x[:5] for x in cabs_list if ('-' not in x)&
                 ('В' not in x)&
                 ('C' not in x)&
                 ('O' not in x)&
                 ('С' not in x)&
                 ('B' not in x)&
                 ('ф' not in x)&
                 ('i' not in x)]
    update.callback_query.message.edit_text(f'{day} \n{time} \n------------\n{", ".join(sorted(cabs_list))}')
def Wednesday_menu_keyboard():
    keyboard = [[InlineKeyboardButton('8:00:00 - 8:50:00', callback_data='Wednesday,08:00:00 - 8:50:00')],
                [InlineKeyboardButton('9:00:00 - 9:50:00', callback_data='Wednesday,09:00:00 - 9:50:00')],
                [InlineKeyboardButton('10:00:00 - 10:50:00', callback_data='Wednesday,10:00:00 - 10:50:00')],
                [InlineKeyboardButton('11:00:00 - 11:50:00', callback_data='Wednesday,11:00:00 - 11:50:00')],
                [InlineKeyboardButton('12:10:00 - 13:00:00', callback_data='Wednesday,12:10:00 - 13:00:00')],
                [InlineKeyboardButton('13:10:00 - 14:00:00', callback_data='Wednesday,13:10:00 - 14:00:00')],
                [InlineKeyboardButton('14:10:00 - 15:00:00', callback_data='Wednesday,14:10:00 - 15:00:00')],
                [InlineKeyboardButton('15:10:00 - 16:00:00', callback_data='Wednesday,15:10:00 - 16:00:00')],
                [InlineKeyboardButton('16:10:00 - 17:00:00', callback_data='Wednesday,16:10:00 - 17:00:00')],
                [InlineKeyboardButton('17:20:00 - 18:10:00', callback_data='Wednesday,17:20:00 - 18:10:00')],
                [InlineKeyboardButton('18:30:00 - 19:20:00', callback_data='Wednesday,18:30:00 - 19:20:00')],
                [InlineKeyboardButton('19:30:00 - 20:20:00', callback_data='Wednesday,19:30:00 - 20:20:00')],
                [InlineKeyboardButton('20:30:00 - 21:20:00', callback_data='Wednesday,20:30:00 - 21:20:00')],
                [InlineKeyboardButton('21:30:00 - 22:20:00', callback_data='Wednesday,21:30:00 - 22:20:00')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def Wednesday_menu_message():
    return 'Choose time in Wednesday menu:'
    
def Thursday_menu(update,context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                            text=Thursday_menu_message(),
                            reply_markup=Thursday_menu_keyboard())
            
def Thursday_submenu(update,context):
    query = update.callback_query
    query.answer()
    day = update.callback_query.data.split(',')[0]
    time = update.callback_query.data.split(',')[1]
    free_cabs = pd.read_excel(r'C:\Users\Dair\Desktop\magnum\Free Cabinets.xlsx', header = 2)#.pivot(index = 'Time', columns = 'Day', values = 'Cabinet')
    free_cabs['Time'] = free_cabs['Time'].apply(lambda x: '0' + x if len(x) < 18 else x)
    free_cabs['begin'] = free_cabs['Time'].apply(lambda x: x[0:8])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs['end'] = free_cabs['Time'].apply(lambda x: '0' + x[11:19] if len(x) < 19 else x[10:19])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs.columns = free_cabs.columns.str.strip().str.lower()
    cabs_list = free_cabs[(free_cabs['day'] == day)&(free_cabs['time'] == time)]['cabinet'].values
    cabs_list = [x[:5] for x in cabs_list if ('-' not in x)&
                 ('В' not in x)&
                 ('C' not in x)&
                 ('O' not in x)&
                 ('С' not in x)&
                 ('B' not in x)&
                 ('ф' not in x)&
                 ('i' not in x)]
    update.callback_query.message.edit_text(f'{day} \n{time} \n------------\n{", ".join(sorted(cabs_list))}')
def Thursday_menu_keyboard():
    keyboard = [[InlineKeyboardButton('8:00:00 - 8:50:00', callback_data='Thursday,08:00:00 - 8:50:00')],
                [InlineKeyboardButton('9:00:00 - 9:50:00', callback_data='Thursday,09:00:00 - 9:50:00')],
                [InlineKeyboardButton('10:00:00 - 10:50:00', callback_data='Thursday,10:00:00 - 10:50:00')],
                [InlineKeyboardButton('11:00:00 - 11:50:00', callback_data='Thursday,11:00:00 - 11:50:00')],
                [InlineKeyboardButton('12:10:00 - 13:00:00', callback_data='Thursday,12:10:00 - 13:00:00')],
                [InlineKeyboardButton('13:10:00 - 14:00:00', callback_data='Thursday,13:10:00 - 14:00:00')],
                [InlineKeyboardButton('14:10:00 - 15:00:00', callback_data='Thursday,14:10:00 - 15:00:00')],
                [InlineKeyboardButton('15:10:00 - 16:00:00', callback_data='Thursday,15:10:00 - 16:00:00')],
                [InlineKeyboardButton('16:10:00 - 17:00:00', callback_data='Thursday,16:10:00 - 17:00:00')],
                [InlineKeyboardButton('17:20:00 - 18:10:00', callback_data='Thursday,17:20:00 - 18:10:00')],
                [InlineKeyboardButton('18:30:00 - 19:20:00', callback_data='Thursday,18:30:00 - 19:20:00')],
                [InlineKeyboardButton('19:30:00 - 20:20:00', callback_data='Thursday,19:30:00 - 20:20:00')],
                [InlineKeyboardButton('20:30:00 - 21:20:00', callback_data='Thursday,20:30:00 - 21:20:00')],
                [InlineKeyboardButton('21:30:00 - 22:20:00', callback_data='Thursday,21:30:00 - 22:20:00')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def Thursday_menu_message():
    return 'Choose time in Thursday menu:'
    
def Friday_menu(update,context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                            text=Friday_menu_message(),
                            reply_markup=Friday_menu_keyboard())
            
def Friday_submenu(update,context):
    query = update.callback_query
    query.answer()
    day = update.callback_query.data.split(',')[0]
    time = update.callback_query.data.split(',')[1]
    free_cabs = pd.read_excel(r'C:\Users\Dair\Desktop\magnum\Free Cabinets.xlsx', header = 2)#.pivot(index = 'Time', columns = 'Day', values = 'Cabinet')
    free_cabs['Time'] = free_cabs['Time'].apply(lambda x: '0' + x if len(x) < 18 else x)
    free_cabs['begin'] = free_cabs['Time'].apply(lambda x: x[0:8])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs['end'] = free_cabs['Time'].apply(lambda x: '0' + x[11:19] if len(x) < 19 else x[10:19])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs.columns = free_cabs.columns.str.strip().str.lower()
    cabs_list = free_cabs[(free_cabs['day'] == day)&(free_cabs['time'] == time)]['cabinet'].values
    cabs_list = [x[:5] for x in cabs_list if ('-' not in x)&
                 ('В' not in x)&
                 ('C' not in x)&
                 ('O' not in x)&
                 ('С' not in x)&
                 ('B' not in x)&
                 ('ф' not in x)&
                 ('i' not in x)]
    update.callback_query.message.edit_text(f'{day} \n{time} \n------------\n{", ".join(sorted(cabs_list))}')
def Friday_menu_keyboard():
    keyboard = [[InlineKeyboardButton('8:00:00 - 8:50:00', callback_data='Friday,08:00:00 - 8:50:00')],
                [InlineKeyboardButton('9:00:00 - 9:50:00', callback_data='Friday,09:00:00 - 9:50:00')],
                [InlineKeyboardButton('10:00:00 - 10:50:00', callback_data='Friday,10:00:00 - 10:50:00')],
                [InlineKeyboardButton('11:00:00 - 11:50:00', callback_data='Friday,11:00:00 - 11:50:00')],
                [InlineKeyboardButton('12:10:00 - 13:00:00', callback_data='Friday,12:10:00 - 13:00:00')],
                [InlineKeyboardButton('13:10:00 - 14:00:00', callback_data='Friday,13:10:00 - 14:00:00')],
                [InlineKeyboardButton('14:10:00 - 15:00:00', callback_data='Friday,14:10:00 - 15:00:00')],
                [InlineKeyboardButton('15:10:00 - 16:00:00', callback_data='Friday,15:10:00 - 16:00:00')],
                [InlineKeyboardButton('16:10:00 - 17:00:00', callback_data='Friday,16:10:00 - 17:00:00')],
                [InlineKeyboardButton('17:20:00 - 18:10:00', callback_data='Friday,17:20:00 - 18:10:00')],
                [InlineKeyboardButton('18:30:00 - 19:20:00', callback_data='Friday,18:30:00 - 19:20:00')],
                [InlineKeyboardButton('19:30:00 - 20:20:00', callback_data='Friday,19:30:00 - 20:20:00')],
                [InlineKeyboardButton('20:30:00 - 21:20:00', callback_data='Friday,20:30:00 - 21:20:00')],
                [InlineKeyboardButton('21:30:00 - 22:20:00', callback_data='Friday,21:30:00 - 22:20:00')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def Friday_menu_message():
    return 'Choose time in Friday menu:'
    
def Saturday_menu(update,context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                            text=Saturday_menu_message(),
                            reply_markup=Saturday_menu_keyboard())
            
def Saturday_submenu(update,context):
    query = update.callback_query
    query.answer()
    day = update.callback_query.data.split(',')[0]
    time = update.callback_query.data.split(',')[1]
    free_cabs = pd.read_excel(r'C:\Users\Dair\Desktop\magnum\Free Cabinets.xlsx', header = 2)#.pivot(index = 'Time', columns = 'Day', values = 'Cabinet')
    free_cabs['Time'] = free_cabs['Time'].apply(lambda x: '0' + x if len(x) < 18 else x)
    free_cabs['begin'] = free_cabs['Time'].apply(lambda x: x[0:8])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs['end'] = free_cabs['Time'].apply(lambda x: '0' + x[11:19] if len(x) < 19 else x[10:19])
    free_cabs['begin'] = pd.to_datetime(free_cabs['begin'], format='%H:%M:%S').dt.time
    free_cabs.columns = free_cabs.columns.str.strip().str.lower()
    cabs_list = free_cabs[(free_cabs['day'] == day)&(free_cabs['time'] == time)]['cabinet'].values
    cabs_list = [x[:5] for x in cabs_list if ('-' not in x)&
                 ('В' not in x)&
                 ('C' not in x)&
                 ('O' not in x)&
                 ('С' not in x)&
                 ('B' not in x)&
                 ('ф' not in x)&
                 ('i' not in x)]
    update.callback_query.message.edit_text(f'{day} \n{time} \n------------\n{", ".join(sorted(cabs_list))}')
def Saturday_menu_keyboard():
    keyboard = [[InlineKeyboardButton('8:00:00 - 8:50:00', callback_data='Saturday,08:00:00 - 8:50:00')],
                [InlineKeyboardButton('9:00:00 - 9:50:00', callback_data='Saturday,09:00:00 - 9:50:00')],
                [InlineKeyboardButton('10:00:00 - 10:50:00', callback_data='Saturday,10:00:00 - 10:50:00')],
                [InlineKeyboardButton('11:00:00 - 11:50:00', callback_data='Saturday,11:00:00 - 11:50:00')],
                [InlineKeyboardButton('12:10:00 - 13:00:00', callback_data='Saturday,12:10:00 - 13:00:00')],
                [InlineKeyboardButton('13:10:00 - 14:00:00', callback_data='Saturday,13:10:00 - 14:00:00')],
                [InlineKeyboardButton('14:10:00 - 15:00:00', callback_data='Saturday,14:10:00 - 15:00:00')],
                [InlineKeyboardButton('15:10:00 - 16:00:00', callback_data='Saturday,15:10:00 - 16:00:00')],
                [InlineKeyboardButton('16:10:00 - 17:00:00', callback_data='Saturday,16:10:00 - 17:00:00')],
                [InlineKeyboardButton('17:20:00 - 18:10:00', callback_data='Saturday,17:20:00 - 18:10:00')],
                [InlineKeyboardButton('18:30:00 - 19:20:00', callback_data='Saturday,18:30:00 - 19:20:00')],
                [InlineKeyboardButton('19:30:00 - 20:20:00', callback_data='Saturday,19:30:00 - 20:20:00')],
                [InlineKeyboardButton('20:30:00 - 21:20:00', callback_data='Saturday,20:30:00 - 21:20:00')],
                [InlineKeyboardButton('21:30:00 - 22:20:00', callback_data='Saturday,21:30:00 - 22:20:00')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def Saturday_menu_message():
    return 'Choose time in Saturday menu:'


# def free_cabs(update, _):
#     menu_main = [[InlineKeyboardButton('Понедельник', callback_data='Monday')],
#                  [InlineKeyboardButton('Вторник', callback_data='Tuesday')],
#                  [InlineKeyboardButton('Среда', callback_data='Wednesday')],
#                  [InlineKeyboardButton('Четверг', callback_data='Thursday')],
#                  [InlineKeyboardButton('Пятница', callback_data='Friday')],
#                  [InlineKeyboardButton('Суббота', callback_data='Saturday')]
#                  ]
#     reply_markup = InlineKeyboardMarkup(menu_main)
#     update.message.reply_text('Выберете день:', reply_markup=reply_markup)

# def menu_actions(update: Update, context: CallbackContext):
#     query = update.callback_query
#     if True:
#         # first submenu
#         menu_1 = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
#                   [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')]]
#         reply_markup = InlineKeyboardMarkup(menu_1)
#         bot.edit_message_text(chat_id=query.message.chat_id,
#                               message_id=query.message.message_id,
#                               text='Выберете время:',
#                               reply_markup=reply_markup)

#         update.message.reply_text(''.format(update.callback_query.data))
# def main_menu(update,context):
#     # keyboard = [[InlineKeyboardButton("Hackerearth", callback_data='asd'),
#     #                      InlineKeyboardButton("Hackerrank", callback_data='HRlist8')],
#     #                     [InlineKeyboardButton("Codechef", callback_data='CClist8'),
#     #                      InlineKeyboardButton("Spoj", callback_data='SPlist8')],
#     #                     [InlineKeyboardButton("Codeforces", callback_data='CFlist8'),
#     #                      InlineKeyboardButton("ALL", callback_data='ALLlist8')]]
#     # reply_markup = InlineKeyboardMarkup(keyboard)
#     # update.message.reply_text('please select the judge or select all for showing all',
#     #                                   reply_markup=reply_markup)

#     # return InlineKeyboardMarkup(keyboard)
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(
#                         text=main_menu_message(),
#                         reply_markup=main_menu_keyboard())
# def first_submenu(bot, update):
#   pass

# def first_menu(update,context):
#   query = update.callback_query
#   query.answer()
#   query.edit_message_text(
#                         text=first_menu_message(),
#                         reply_markup=first_menu_keyboard())
# def main_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
#               [InlineKeyboardButton('Option 2', callback_data='m2')],
#               [InlineKeyboardButton('Option 3', callback_data='m3')]]
#   return InlineKeyboardMarkup(keyboard)

# def first_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
#               [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
#               [InlineKeyboardButton('Main menu', callback_data='main')]]
#   return InlineKeyboardMarkup(keyboard)

# def main_menu_message():
#   return 'Choose the option in main menu:'

# def first_menu_message():
#   return 'Choose the submenu in first menu:'

def how_to_rk1(update, _):
    update.message.reply_photo(
        open('image.psd (2).png','rb'),
        reply_markup=ReplyKeyboardRemove(),
        caption = 'Как читается график?\n'
        'Очень просто. по оси OX - возможные оценки на экзамене, по оси OY - возможные исходы тотала.\n'
        'Зеленые плитки - исходы, при которых ты останешься на стипендии, желтые - слетаешь.\n'
        'Нужно узнать свою оценку за рк1, например, 67.\n'
        'Затем смотрим на OY, прикидываем, сколько получим на рк2, допустим, 75 и делаем выводы, что нам нужно'
        'получить 65+ на экзамене, чтобы остаться на стипендии.\n'
        'Все расчеты сделаны по формуле плоскости в пространстве и формуле конченой оценки\n'
        '------------\n'
        'total = 0.3*rk1 + 0.3*rk2 + 0.4*exam\n'
        '------------\n'
        'Почему оси начинаются с 50, а не с 0?\n'
        'Потому-что это минимальный балл, который можно получить на рк и экзамене, все, что ниже - пересдача'
    )
    return ConversationHandler.END

def how_to_rksrd(update, _):
    update.message.reply_photo(
        open('image.psd (3).png','rb'),
        reply_markup=ReplyKeyboardRemove(),
        caption = 'Как читается график?\n'
        'Очень просто. по оси OX - возможные оценки на экзамене, по оси OY - возможные исходы тотала.\n'
        'Все, что находится справа от зеленой линии - исходы, при которых ты остаешься на стипендии,\n'
        'все, что находится между зеленой и красной - исходы, при которых ты слетаешь.'
        'Нужно узнать свою оценку за рксрд, например, 67.\n'
        'смотрим на зеленое число(справа от горизонтальной зеленой линнии) - это минимальная граница баллов на экзамене для стипендии\n'
        'В этом случае тебе надо набрать 74.50+ на экзамене, чтобы остаться на стипендии\n'
        'Красная линия - минмальный тотал, который может выйти. (при оценке на экзамене в 50 баллов)\n'
        'в нашем случае это 60.20'
        'Все расчеты сделаны по формуле прямой на плоскости и формуле конченой оценки\n'
        '------------\n'
        'total = 0.3*rk1 + 0.3*rk2 + 0.4*exam\n'
        '------------\n'
        'Почему 60.20 - минимальная оценка?\n'
        'Потому-что минимальный балл, который можно получить на экзамене, это 50, что ниже - пересдача'
    )
    return ConversationHandler.END
# def asd(update, _):
#     # Список кнопок для ответа
#     reply_keyboard1 = [['график', 'гороскоп']]
#     # Создаем простую клавиатуру для ответа
#     markup_key1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)
#     # Начинаем разговор с вопроса
#     update.message.reply_text(
#         'отправь график для графика'
#         'отправь гороскоп для гороскопа'
#         'Команда /cancel, чтобы прекратить разговор.\n\n',
#         reply_markup=markup_key1)
#     # переходим к этапу `GENDER`, это значит, что ответ
#     # отправленного сообщения в виде кнопок будет список 
#     # обработчиков, определенных в виде значения ключа `GENDER`
#     return PLOT

def plot(update, _):
    # Список кнопок для ответа

    reply_keyboard = [['рк1', 'рксрд', 'рк1 и рк2']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    # update.message.reply_text(
    #     '',
        
    #         reply_markup=ReplyKeyboardRemove())
    # reply_keyboard = [
    #             [InlineKeyboardButton("Click button 1", callback_data='callback_1')],
    #             [InlineKeyboardButton("Click button 1", callback_data='callback_2')]
    #         ]
    # markup_key = InlineKeyboardMarkup(reply_keyboard)
    # message_reply_text = 'Click one of these buttons'
    update.message.reply_text(
        'на основе оценки за какой рк ты хочешь'
        'посмотреть анализ?'
        'Команда /cancel, чтобы прекратить разговор.\n\n',
        reply_markup=markup_key)
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список 
    # обработчиков, определенных в виде значения ключа `GENDER`
    return GENDER

def gender(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал пол пользователя
    logger.info("выбор %s: %s", user.first_name, update.message.text)
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    if update.message.text == 'рк1':
        update.message.reply_text(
        'отправь свою оценку за рк1\n /cancel - для отмены', reply_markup=ReplyKeyboardRemove())
        return PHOTO
    if update.message.text == 'рксрд':
        update.message.reply_text(
        'отправь свою оценку за рксрд\n /cancel - для отмены', reply_markup=ReplyKeyboardRemove())
        return PHOTO2
    if update.message.text == 'рк1 и рк2':
        update.message.reply_text(
        'отправь свои оценки за рк1 и рк2 через запятую,пожалуйста\n /cancel - для отмены', reply_markup=ReplyKeyboardRemove())
        return PHOTO3

def transit3(update, _):
    if update.message.text == '/cancel':
            update.message.reply_text(
            'Действие отменено', 
            reply_markup=ReplyKeyboardRemove()
                )
            # Заканчиваем разговор.
            return ConversationHandler.END
    update.message.reply_text(
    'отправь свои оценки за рк1 и рк2, еще раз, пожалуйста\n /cancel - для отмены')
    return PHOTO2

def photo3(update, _):
    try:
        rk1 = re.findall(r"(\d+(?:\.\d+)?)", update.message.text)[0]
        rk2 = re.findall(r"(\d+(?:\.\d+)?)", update.message.text)[1]
        temp = 1 / (max(float(rk1) - 50, 0)*(max(100-float(rk1), 0)))
        temp = 1 / (max(float(rk2) - 50, 0)*(max(100-float(rk2), 0)))
        rksrd = 0.5*float(rk1) + float(rk2)*0.5
    # if 50 <= float(rksrd) <= 100:
        # pass
    # else:
        del temp
    except:
        if update.message.text == '/cancel':
            update.message.reply_text(
            'Действие отменено', 
            reply_markup=ReplyKeyboardRemove()
                )
            # Заканчиваем разговор.
            return ConversationHandler.END
        update.message.reply_text('отправьте, пожалуйста, реальне оценки\n (50-100)\n /cancel - для отмены')
        return TRANSIT3
    rksrd = float(rksrd)
    fig = plt.figure(figsize = (20,15))
    ax = plt.axes()
    x = np.linspace(0, 100, 2)
    y = np.array([rksrd * 0.6 + 0.4 * i for i in x])
    sns.set(font_scale = 2)
    plt.xlabel('Exam', size = 40)
    plt.ylabel('Final', size = 40)
    ax.plot(x, y, color = 'blue', linewidth=2);
    ax.plot([50, 50], [rksrd * 0.6, rksrd * 0.6 + 50 * 0.4], linewidth=2, color = 'red')
    ax.plot([50, 0], [rksrd * 0.6 + 50 * 0.4, rksrd * 0.6 + 50 * 0.4], linewidth=2, color = 'red')
    if 0 <= (70 - rksrd * 0.6) / 0.4 <= 100:
        ax.plot([(70 - rksrd * 0.6) / 0.4, (70 - rksrd * 0.6) / 0.4], [0.6 * rksrd, 70], linewidth=2, color = 'green')
        ax.plot([0, (70 - rksrd * 0.6) / 0.4], [70, 70], linewidth=2, color = 'green')
        plt.text((70 - rksrd * 0.6) / 0.4 + 0.5, (70 + (rksrd * 0.6))/2, f'{(70 - rksrd * 0.6) / 0.4:.2f}', color = 'green')

    plt.text(25 , rksrd * 0.6 + 50 * 0.4 + 0.5, f'{rksrd * 0.6 + 50 * 0.4:.2f}', color = 'red')
    plt.text(25 , rksrd * 0.6 + 50 * 0.4 + 0.5, f'{rksrd * 0.6 + 50 * 0.4:.2f}', color = 'red')
    plt.title(f'Final grade depending on the exam for {rksrd}', size = 60)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.tick_params(axis='both', which='minor', labelsize=25)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    update.message.reply_photo(
        buf,
        reply_markup=ReplyKeyboardRemove(),
    )
    plt.close('all')
    return ConversationHandler.END

def transit2(update, _):
    if update.message.text == '/cancel':
            update.message.reply_text(
            'Действие отменено', 
            reply_markup=ReplyKeyboardRemove()
                )
            # Заканчиваем разговор.
            return ConversationHandler.END
    update.message.reply_text(
    'отправь свою оценку за рксрд, еще раз, пожалуйста\n /cancel - для отмены')
    return PHOTO2

def photo2(update, _):
    try:
        rksrd = re.search(r"(\d+(?:\.\d+)?)", update.message.text.replace(',', '.')).group()
        temp = 1 / (max(float(rksrd) - 50, 0)*(max(100-float(rksrd), 0)))
    # if 50 <= float(rksrd) <= 100:
        # pass
    # else:
        del temp
    except:
        if update.message.text == '/cancel':
            update.message.reply_text(
            'Действие отменено', 
            reply_markup=ReplyKeyboardRemove()
                )
            # Заканчиваем разговор.
            return ConversationHandler.END
        update.message.reply_text('отправьте, пожалуйста, реальную оценку\n (50-100)\n /cancel - для отмены')
        return TRANSIT2
    rksrd = float(rksrd)
    fig = plt.figure(figsize = (20,15))
    ax = plt.axes()
    x = np.linspace(0, 100, 2)
    y = np.array([rksrd * 0.6 + 0.4 * i for i in x])
    sns.set(font_scale = 2)
    plt.xlabel('Exam', size = 40)
    plt.ylabel('Final', size = 40)
    ax.plot(x, y, color = 'blue', linewidth=2);
    ax.plot([50, 50], [rksrd * 0.6, rksrd * 0.6 + 50 * 0.4], linewidth=2, color = 'red')
    ax.plot([50, 0], [rksrd * 0.6 + 50 * 0.4, rksrd * 0.6 + 50 * 0.4], linewidth=2, color = 'red')
    if 0 <= (70 - rksrd * 0.6) / 0.4 <= 100:
        ax.plot([(70 - rksrd * 0.6) / 0.4, (70 - rksrd * 0.6) / 0.4], [0.6 * rksrd, 70], linewidth=2, color = 'green')
        ax.plot([0, (70 - rksrd * 0.6) / 0.4], [70, 70], linewidth=2, color = 'green')
        plt.text((70 - rksrd * 0.6) / 0.4 + 0.5, (70 + (rksrd * 0.6))/2, f'{(70 - rksrd * 0.6) / 0.4:.2f}', color = 'green')

    plt.text(25 , rksrd * 0.6 + 50 * 0.4 + 0.5, f'{rksrd * 0.6 + 50 * 0.4:.2f}', color = 'red')
    plt.text(25 , rksrd * 0.6 + 50 * 0.4 + 0.5, f'{rksrd * 0.6 + 50 * 0.4:.2f}', color = 'red')
    plt.title(f'Final grade depending on the exam for {rksrd}', size = 60)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.tick_params(axis='both', which='minor', labelsize=25)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    update.message.reply_photo(
        buf,
        reply_markup=ReplyKeyboardRemove(),
    )
    plt.close('all')
    return ConversationHandler.END

def transit(update, _):
    
    if update.message.text == '/cancel':
            update.message.reply_text(
            'Действие отменено', 
            reply_markup=ReplyKeyboardRemove()
                )
            # Заканчиваем разговор.
            return ConversationHandler.END
    update.message.reply_text(
    'отправь свою оценку за рк1, еще раз, пожалуйста\n /cancel - для отмены')
    return PHOTO

def photo(update, _):
    rcParams.update({'figure.autolayout': True})
    user = update.message.from_user
    # Пишем в журнал пол пользователя
    logger.info("Пол %s: %s", user.first_name, update.message.text)
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    try:
        rk1 = re.search(r"(\d+(?:\.\d+)?)", update.message.text.replace(',', '.')).group()
        temp = 1 / (max(float(rk1) - 50, 0)*(max(100-float(rk1), 0)))
    # if 50 <= float(rk1) <= 100:
    #     pass
    # else:
        del temp
    except:
        if update.message.text == '/cancel':
            update.message.reply_text(
            'Действие отменено', 
            reply_markup=ReplyKeyboardRemove()
                )
            # Заканчиваем разговор.
            return ConversationHandler.END
        update.message.reply_text('отправьте, пожалуйста, реальную оценку\n (50-100)\n /cancel - для отмены')
        return TRANSIT

    a,b,c,d = 0.3, 0.4, -1, -0.3 * float(rk1)
    x = np.linspace(51,100,30)
    y = np.linspace(51,100,30)

    X,Y = np.meshgrid(x,y)
    Z = (d - a*X - b*Y) / c
    zxc = pd.DataFrame(Z)
    for i in pd.DataFrame(Z).columns:
        zxc[i] = zxc[i].apply(lambda x : 0 if x <= 50 else (1 if x <= 70 else 2))
    asd = pd.DataFrame(Y)
    for i in pd.DataFrame(Z).columns:
        asd[i] = asd[i].apply(lambda x : 0 if x <= 50 else 1)
    qwe = pd.DataFrame(X)
    for i in pd.DataFrame(X).columns:
        qwe[i] = qwe[i].apply(lambda x : 0 if x <= 50 else 1)
    fgh = pd.DataFrame(columns = qwe.columns)
    for i in pd.DataFrame(X).columns:
        fgh[i] = fgh[i].apply(lambda x : 0)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.gcf().set_size_inches(20, 15)
    plt.xlabel('Рк2',  labelpad=35, size = 45)
    plt.ylabel('Exam',  labelpad=35, size = 45)
    ax.zaxis.set_rotate_label(False)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    ax.set_zticks(np.arange(0, min(float(rk1)+20, 100), 20), fontsize = 35)
    ax.set_zlabel('Final', fontsize=45, rotation = 0, labelpad=35)
    surf = ax.scatter(X, Y, Z, s = 100, c=(qwe*asd*zxc).values, cmap= colors.ListedColormap(['yellow', 'green']), linewidth=0.5)
    ax.scatter(X, Y, Z*0, s = 100, c=(qwe*asd*zxc).values, alpha = 0.3, cmap= colors.ListedColormap(['yellow', 'green']), linewidth=0.5)
    plt.title('Final grade depending \n on the exam and rk2 for %.2f' %float(rk1), size = 60, y=1.09)
    # chat_id = bot.get_updates()[-1].message.chat_id
    # bot.send_photo(chat_id, plt)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    update.message.reply_photo(
        buf,
        reply_markup=ReplyKeyboardRemove(),
    )
    plt.close('all')
    x = np.linspace(51,100,10)
    y = np.linspace(51,100,10)
    X,Y = np.meshgrid(x,y)
    a,b,c,d = 0.3, 0.4, -1, -0.3 * float(rk1)
    Z = (d - a*X - b*Y) / c
    zxc = pd.DataFrame(Z)
    for i in pd.DataFrame(Z).columns:
        zxc[i] = zxc[i].apply(lambda x : 0 if x <= 50 else (1 if x <= 70 else 2))
    asd = pd.DataFrame(Y)
    for i in pd.DataFrame(Z).columns:
        asd[i] = asd[i].apply(lambda x : 0 if x <= 50 else 1)
    qwe = pd.DataFrame(X)
    for i in pd.DataFrame(X).columns:
        qwe[i] = qwe[i].apply(lambda x : 0 if x <= 50 else 1)
    g = sns.heatmap(pd.DataFrame((qwe*asd*zxc).values,
                             columns = [x[0] for x in X],
                             index = [x[0] for x in Y]),
                cmap= colors.ListedColormap([ 'yellow', 'green']),
                cbar=False,
                linewidths=4
               )
    g.set_xticks(range(10))
    g.set_xticklabels([x for x in np.arange(50,100, 5)], size = 60, rotation = -45)
    g.set_yticks(range(10))
    g.set_yticklabels([x for x in np.arange(50,100, 5)], size = 60)
    plt.gcf().set_size_inches(20, 15)
    plt.ylabel('Exam',  size = 60, rotation = 0, labelpad=100)
    plt.xlabel('Рк2',  size = 60)
    plt.title(f'Final grade depending \non the exam and rk2 for {rk1}', size = 80, y=1.09)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    update.message.reply_photo(
        buf,
        reply_markup=ReplyKeyboardRemove()
    )
    plt.close('all')
    # update.message.reply_text(user.gender)
    # переходим к этапу `PHOTO`
    return ConversationHandler.END

# def secondplot(update, _):
#     x = np.linspace(51,100,10)
#     y = np.linspace(51,100,10)
#     X,Y = np.meshgrid(x,y)
#     a,b,c,d = 0.3, 0.4, -1, -0.3 * float(rk1)
#     Z = (d - a*X - b*Y) / c
#     zxc = pd.DataFrame(Z)
#     for i in pd.DataFrame(Z).columns:
#         zxc[i] = zxc[i].apply(lambda x : 0 if x <= 50 else (1 if x <= 70 else 2))
#     asd = pd.DataFrame(Y)
#     for i in pd.DataFrame(Z).columns:
#         asd[i] = asd[i].apply(lambda x : 0 if x <= 50 else 1)
#     qwe = pd.DataFrame(X)
#     for i in pd.DataFrame(X).columns:
#         qwe[i] = qwe[i].apply(lambda x : 0 if x <= 50 else 1)
#     g = sns.heatmap(pd.DataFrame((qwe*asd*zxc).values,
#                              columns = [x[0] for x in X],
#                              index = [x[0] for x in Y]),
#                 cmap= colors.ListedColormap([ 'yellow', 'green']),
#                 cbar=False,
#                 linewidths=4
#                )
#     g.set_xticks(range(10))
#     g.set_xticklabels([x for x in np.arange(50,100, 5)], size = 60, rotation = -45)
#     g.set_yticks(range(10))
#     g.set_yticklabels([x for x in np.arange(50,100, 5)], size = 60)
#     plt.gcf().set_size_inches(20, 15)
#     plt.ylabel('Exam',  size = 60, rotation = 0, labelpad=100)
#     plt.xlabel('Рк2',  size = 60)
#     plt.title('Final grade depending on the exam and rk2', size = 80, y=1.09)
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     update.message.reply_photo(
#         buf,
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     # update.message.reply_text(user.gender)
#     # переходим к этапу `PHOTO`
#     return ConversationHandler.END

# updater = Updater("5637376738:AAEliHovXHBx6O_0pKcIRePBgEOR8S9N8xU",
#                   use_context=True)
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Извини, я не понимаю, о чем ты '%s'" % update.message.text)
  
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Извини, но нет такой команды %s" % update.message.text)

# def press_button_callback(bot, update):
#     seed(1)
#     random_number = str(random())
#     keyboard = [
#                 [InlineKeyboardButton('Click button 1' , callback_data='callback_1')],
#                 [InlineKeyboardButton('Click button 1 ' + random_number, callback_data='callback_2')]
#             ]

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.callback_query.edit_message_reply_markup(reply_markup)
if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater("5637376738:AAEliHovXHBx6O_0pKcIRePBgEOR8S9N8xU")
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # updater.dispatcher.add_handler(CallbackQueryHandler(press_button_callback))
    # Определяем обработчик разговоров `ConversationHandler` 
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    # conv_handler = ConversationHandler( # здесь строится логика разговора
    #     # точка входа в разговор
    #     entry_points=[CommandHandler('start', start)],
    #     # этапы разговора, каждый со своим списком обработчиков сообщений
    #     states={
    #         PLOT : [MessageHandler(Filters.regex('^(график|гороскоп)$'), plot)],
    #         GENDER: [MessageHandler(Filters.regex('^(рк1|рксрд|рк1 и рк2)$'), gender)]
    #     },
    #     # точка выхода из разговора
    #     fallbacks=[CommandHandler('cancel', cancel)],
    #     run_async=True
    # )
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('how_to_rk1', how_to_rk1))
    updater.dispatcher.add_handler(CommandHandler('how_to_rksrd', how_to_rksrd))
    # updater.dispatcher.add_handler(CommandHandler('free_cabs', free_cabs))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('free_cabs', free_cabs))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='^main$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(Monday_menu, pattern='^m1$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(Tuesday_menu, pattern='^m2$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(Wednesday_menu, pattern='^m3$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(Thursday_menu, pattern='^m4$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(Friday_menu, pattern='^m5$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(Saturday_menu, pattern='^m6$'))

    updater.dispatcher.add_handler(CallbackQueryHandler(Monday_submenu,
                                                        pattern=''))
    updater.dispatcher.add_handler(CallbackQueryHandler(Tuesday_submenu,
                                                        pattern=''))
    updater.dispatcher.add_handler(CallbackQueryHandler(Wednesday_submenu,
                                                        pattern=''))
    updater.dispatcher.add_handler(CallbackQueryHandler(Thursday_submenu,
                                                        pattern=''))
    updater.dispatcher.add_handler(CallbackQueryHandler(Friday_submenu,
                                                        pattern=''))
    updater.dispatcher.add_handler(CallbackQueryHandler(Saturday_submenu,
                                                        pattern=''))

    # dispatcher.add_handler(CallbackQueryHandler(menu_actions))
    # updater.dispatcher.add_handler(CommandHandler('main_menu', main_menu))
    # updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    # # updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
    #                                                     pattern='m1_1'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
    #                                                     pattern='m2_1'))
    conv_handler2 = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('plot', plot)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            PLOT : [MessageHandler(Filters.regex('^(график)$'), plot)],
            # GENDER: [MessageHandler(Filters.regex('^(рк1|рксрд|рк1 и рк2)$'), gender)],
            GENDER: [MessageHandler(Filters.regex(''), gender)],
            PHOTO: [MessageHandler(Filters.regex(''), photo)],
            TRANSIT : [MessageHandler(Filters.regex(''), transit)],
            PHOTO2: [MessageHandler(Filters.regex(''), photo2)],
            TRANSIT2 : [MessageHandler(Filters.regex(''), transit2)],
            PHOTO3: [MessageHandler(Filters.regex(''), photo3)],
            TRANSIT3 : [MessageHandler(Filters.regex(''), transit3)]
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
        run_async=True
    )
    # def handle_error(error, update):
    #     tb = traceback.format_exc()
    #     print("got the error:" + str(error)+"\nMore info:" + str(tb) , error=True)
    #     print(tb)
    #     message = "Ops! Error😞"
    #     keyboard = [[InlineKeyboardButton("Close❌", callback_data='cancel')],
    #                 [InlineKeyboardButton("Menù🏠↩️", callback_data='help')]]
    #     reply_markup = InlineKeyboardMarkup(keyboard,
    #                                     one_time_keyboard=True,
    #                                     resize_keyboard=True)
    #     if update.message != None:
    #         update.message.reply_text(message, reply_markup=reply_markup,parse_mode=ParseMode.HTML)
    #     else:
    #         updater.bot.answerCallbackQuery(update.callback_query.id)
    #         update.callback_query.edit_message_text(message, reply_markup=reply_markup,parse_mode=ParseMode.HTML)

    #     return HANDLE_ERROR
    # Добавляем обработчик разговоров `conv_handler`
    # dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(conv_handler2)
    # dispatcher.add_error_handler(error)
    # dispatcher.add_error_handler(handle_error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  
# Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    # Запуск бота
    updater.start_polling()
    updater.idle()
# def start(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         "Enter the text you want to show to the user whenever they start the bot")

# def help(update: Update, context: CallbackContext):
#     update.message.reply_text("Your Message")

# def score_on_rk1(update: Update, context: CallbackContext):
#     update.message.reply_text("Напишите оценку за рк1")
#     time.sleep(5)
#     update.message.reply_text(update.message.text)
    
# def gmail_url(update: Update, context: CallbackContext):
#     update.message.reply_text("gmail link here")

# def youtube_url(update: Update, context: CallbackContext):
#     update.message.reply_text("youtube link")
    
# def linkedIn_url(update: Update, context: CallbackContext):
#     update.message.reply_text("Your linkedin profile url")

# def geeks_url(update: Update, context: CallbackContext):
#     update.message.reply_text("GeeksforGeeks url here")

# def unknown_text(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         "Sorry I can't recognize you , you said '%s'" % update.message.text)

# def unknown(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         "Sorry '%s' is not a valid command" % update.message.text)

# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
# updater.dispatcher.add_handler(CommandHandler('gmail', gmail_url))
# updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
# updater.dispatcher.add_handler(CommandHandler('huy', score_on_rk1))
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# updater.dispatcher.add_handler(MessageHandler(
#     # Filters out unknown commands
#     Filters.command, unknown))
  
# # Filters out unknown messages.
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

# updater.start_polling()