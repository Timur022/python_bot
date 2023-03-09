# -*- coding: utf-8 -*-
from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import logging
import traceback
import time
import datetime
import mysql.connector
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import subprocess
import bot_rasp
import re
import aiovk


app = Flask(__name__)

vk_session = vk_api.VkApi(token='токен')

vk = vk_session.get_api()

dirr = "/home/sammy/bot/"

logging.basicConfig(filename= dirr + "bot.log", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
log = logging.getLogger("ex")

confirmation_code = '6e1df214'

i = 0
m = ''
week_all = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
week_all_u = ["ВОСКРЕСЕНЬЕ", "ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА"]
B_all = [" ", " Января", " Февраля", " Марта", " Апреля", " Мая", " Июня", " Июля", " Августа", " Сентября", " Октября", " Ноября", " Декабря"]
m_all = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12]
d_all = [[0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
         [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]
Bmon = int(time.strftime('%m'))

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except:
        log.exception(traceback.format_exc())
    return connection

def execute_query(query):
    connection = create_connection("localhost", "root", "BVYuWim1990", "rasp")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def execute_read_query(query):
    connection = create_connection("localhost", "root", "BVYuWim1990", "rasp")
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchall()
    return result

gr = {}
gr = execute_read_query('SELECT groupa FROM activ GROUP BY groupa')
groups = []
for j in gr:
    groups.append(j[0])

aud = {}
aud = execute_read_query('SELECT auditorium FROM raspisanie GROUP BY auditorium')
auditoriums = []
for j in aud:
    auditoriums.append(j[0])

tea = {}
tea = execute_read_query('SELECT Teacher FROM raspisanie GROUP BY Teacher')
Teachers = []
for j in tea:
    Teachers.append(j[0])

dd_all = []
for i in range(1, 32):
    dd_all.append(str(i))

mday_end = 0
if int(time.strftime('%Y')) % 4 == 0:
    mday_end = 1
year = int(time.strftime('%Y'))
mes_all = []
if int(time.strftime('%d')) + 7 > d_all[mday_end][int(time.strftime('%m'))]:
    for i in range(int(time.strftime('%d')), d_all[mday_end][int(time.strftime('%m'))] + 1):
        mes_all.append(i)
    mes_end = (int(time.strftime('%d')) + 7) - d_all[mday_end][int(time.strftime('%m'))]
    for i in range(1, mes_end):
        mes_all.append(i)
else:
    for i in range(int(time.strftime('%d')), int(time.strftime('%d')) + 7):
        mes_all.append(i)

text_mes_d = []
for mes in range(0, 13):
    for day in range(1, d_all[mday_end][mes] + 1):
        text_mes_d.append(str(day) + B_all[mes].upper())

user_user = VkKeyboard(one_time=False)
user_user.add_button("Студент", color=VkKeyboardColor.PRIMARY)
user_user.add_line()
user_user.add_button("Преподаватель", color=VkKeyboardColor.PRIMARY)
user_user.add_line()
user_user.add_button("Аудитория", color=VkKeyboardColor.PRIMARY)

data = VkKeyboard(one_time=False)
data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
data.add_line()
data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
data.add_line()
data.add_button('Изображение \U0001F5BC', color=VkKeyboardColor.PRIMARY) # 1F4C3
data.add_line()
data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT

rand = random.randint(0, len(groups) - 2)
keyboard1 = VkKeyboard(one_time=False)
keyboard1.add_button(groups[rand].replace('_', '-'), color=VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button(groups[rand + 1].replace('_', '-'), color=VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT

rand2 = random.randint(0, len(Teachers) - 2)
keyboard2 = VkKeyboard(one_time=False)
keyboard2.add_button(Teachers[rand2], color=VkKeyboardColor.PRIMARY)
keyboard2.add_line()
keyboard2.add_button(Teachers[rand2 + 1], color=VkKeyboardColor.PRIMARY)
keyboard2.add_line()
keyboard2.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT

rand3 = random.randint(0, len(auditoriums) - 2)
keyboard3 = VkKeyboard(one_time=False)
keyboard3.add_button(auditoriums[rand3], color=VkKeyboardColor.PRIMARY)
keyboard3.add_line()
keyboard3.add_button(auditoriums[rand3 + 1], color=VkKeyboardColor.PRIMARY)
keyboard3.add_line()
keyboard3.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT


nomer = ['1', '2', '3', '4', '5', '6', '7']
par_all = [['8:00-9:35', '9:45-11:20', '11:40-13:15', '13:45-15:20', '15:30-17:05', '17:15-18:15', '18:25-19:25'],
           ['8:00-9:35', '9:45-11:20', '11:30-13:05', '13:35-15:10', '15:20-16:55', '17:05-18:05', '18:15-19:15']]
#par_all = [['8:30-10:00', '10:10-11:40', '11:50-13:20', '13:30-15:00', '15:10-16:40', '16:50-17:50', '18:00-19:00'],
#           ['8:30-10:00', '10:10-11:40', '11:50-13:20', '13:30-15:00', '15:10-16:40', '16:50-17:50', '18:00-19:00']]

stickers_id = [18466, 18467, 18473, 18484]
groups_groups = []
groups_rasps = []

Bmon_a = []

def message_pic(user_, year, Bmon, mes, t_us, event_user_id, week):
    mes_end = d_all[mday_end][int(time.strftime('%m'))]
    h_table = [0, 140, 190, 240, 290, 340, 390, 440, 490, 540, 590, 640, 690, 740, 790, 840, 890, 940, 990]
    date = datetime.date(year, Bmon, mes)
    timetup = date.timetuple()
    title = str(mes) + B_all[Bmon] + ' ' + week_all[int(time.strftime('%w', timetup))]
    c = execute_read_query('SELECT * FROM raspisanie WHERE ' + t_us + ' = "' + str(user_) + '" AND date_r = "' + str(mes) + B_all[Bmon] + '" ORDER BY number_par')
    
    fnt = ImageFont.truetype(dirr + "6622.ttf", 16)

    pos_num_p  = [ 87, 137, 187, 237, 287, 337, 387, 437, 487, 537, 587, 637, 687, 737, 787, 837, 887, 937]
    pos_name_p = [ 85, 135, 185, 235, 285, 335, 385, 435, 485, 535, 585, 635, 685, 735, 785, 835, 885, 935]
    pos_prepod = [110, 160, 210, 260, 310, 360, 410, 460, 510, 560, 610, 660, 710, 760, 810, 860, 910, 960]
    pos_line_b = [130, 180, 230, 280, 330, 380, 430, 480, 530, 580, 630, 680, 730, 780, 830, 880, 910, 980]
    pos_line   = [105, 155, 205, 255, 305, 355, 405, 455, 505, 555, 605, 655, 705, 755, 805, 855, 905, 955]
    title = str(mes) + B_all[Bmon] + ' ' + week_all[int(time.strftime('%w', timetup))]
    if c != []:
        if t_us == 'groupa':
            length_c = len(c)
            img = Image.open(dirr + str(length_c) + '.png')
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(title, font=fnt)
            draw.text((10, 20), title, font=fnt, fill=0)
            groupa_c = c[0][0].replace('_', '-')
            fnt = ImageFont.truetype(dirr + "6622.ttf", 20)
            w, h = draw.textsize(groupa_c, font=fnt)
            draw.text((((500-w)/2), 57), groupa_c, font=fnt, fill=0)
            draw.text((20, 57), '№', font=fnt, fill=0)
            for i in range(0, length_c):
                if c[i][2] != '':
                    if time.strftime('%w', timetup) != '6':
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 30)
                        draw.text((20, pos_num_p[i]), str(c[i][1]), font=fnt, fill=0)
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 14)
                        draw.text((53, pos_name_p[i]), c[i][2], font=fnt, fill=0)
                        draw.text((53, pos_prepod[i]), c[i][4], font=fnt, fill=0)
                        draw.text((343, pos_name_p[i]), c[i][3], font=fnt, fill=0)
                        draw.text((343, pos_prepod[i]), par_all[0][c[i][1]-1], font=fnt, fill=0)
                    else:
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 30)
                        draw.text((20, pos_num_p[i]), str(c[i][1]), font=fnt, fill=0)
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 14)
                        draw.text((53, pos_name_p[i]), c[i][2], font=fnt, fill=0)
                        draw.text((53, pos_prepod[i]), c[i][4], font=fnt, fill=0)
                        draw.text((343, pos_name_p[i]), c[i][3], font=fnt, fill=0)
                        draw.text((343, pos_prepod[i]), par_all[1][c[i][1]-1], font=fnt, fill=0)
        elif t_us == 'auditorium':
            length_c = len(c)

            img = Image.new("RGB", (500, h_table[length_c]), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(title, font=fnt)

            draw.line((10,50, 490,50), fill=0, width=2)
            draw.line((490,50, 490,h_table[length_c]-10), fill=0, width=2)
            draw.line((490,h_table[length_c]-10, 10,h_table[length_c]-10), fill=0, width=2)
            draw.line((10,50, 10,h_table[length_c]-10), fill=0, width=2)
            draw.line((50,50, 50,h_table[length_c]-10), fill=0)
            draw.line((10,80, 490,80), fill=0, width=2)
            draw.line((339,80, 339,h_table[length_c]-10), fill=0)

            draw.text((10, 20), title, font=fnt, fill=0)

            groupa_c = c[0][3] + ' аудитория'
            fnt = ImageFont.truetype(dirr + "6622.ttf", 20)
            w, h = draw.textsize(groupa_c, font=fnt)
            draw.text((((500-w)/2), 57), groupa_c, font=fnt, fill=0)
            draw.text((20, 57), '№', font=fnt, fill=0)

            for i in range(0, length_c):
                draw.line((50,pos_line[i], 490,pos_line[i]), fill=0)
                draw.line((10,pos_line_b[i], 490,pos_line_b[i]), fill=0, width=2)
                if c[i][2] != '':
                    if time.strftime('%w', timetup) != '6':
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 30)
                        draw.text((20, pos_num_p[i]), str(c[i][1]), font=fnt, fill=0)
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 14)
                        draw.text((53, pos_name_p[i]), c[i][2], font=fnt, fill=0)
                        draw.text((53, pos_prepod[i]), c[i][4], font=fnt, fill=0)
                        draw.text((343, pos_name_p[i]), c[i][0], font=fnt, fill=0)
                        draw.text((343, pos_prepod[i]), par_all[0][c[i][1]-1], font=fnt, fill=0)
                    else:
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 30)
                        draw.text((20, pos_num_p[i]), str(c[i][1]), font=fnt, fill=0)
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 14)
                        draw.text((53, pos_name_p[i]), c[i][2], font=fnt, fill=0)
                        draw.text((53, pos_prepod[i]), c[i][4], font=fnt, fill=0)
                        draw.text((343, pos_name_p[i]), c[i][0], font=fnt, fill=0)
                        draw.text((343, pos_prepod[i]), par_all[1][c[i][1]-1], font=fnt, fill=0)
        elif t_us == 'Teacher':
            length_c = len(c)

            img = Image.new("RGB", (500, h_table[length_c]), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(title, font=fnt)

            draw.line((10,50, 490,50), fill=0, width=2)
            draw.line((490,50, 490,h_table[length_c]-10), fill=0, width=2)
            draw.line((490,h_table[length_c]-10, 10,h_table[length_c]-10), fill=0, width=2)
            draw.line((10,50, 10,h_table[length_c]-10), fill=0, width=2)
            draw.line((50,50, 50,h_table[length_c]-10), fill=0)
            draw.line((10,80, 490,80), fill=0, width=2)
            draw.line((339,80, 339,h_table[length_c]-10), fill=0)

            draw.text((10, 20), title, font=fnt, fill=0)

            groupa_c = c[0][4]
            fnt = ImageFont.truetype(dirr + "6622.ttf", 20)
            w, h = draw.textsize(groupa_c, font=fnt)
            draw.text((((500-w)/2), 57), groupa_c, font=fnt, fill=0)
            draw.text((20, 57), '№', font=fnt, fill=0)
            for i in range(0, length_c):
                draw.line((50,pos_line[i], 490,pos_line[i]), fill=0)
                draw.line((10,pos_line_b[i], 490,pos_line_b[i]), fill=0, width=2)
                if c[i][2] != '':
                    if time.strftime('%w', timetup) != '6':
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 30)
                        draw.text((20, pos_num_p[i]), str(c[i][1]), font=fnt, fill=0)
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 14)
                        draw.text((53, pos_name_p[i]), c[i][2], font=fnt, fill=0)
                        draw.text((53, pos_prepod[i]), c[i][0], font=fnt, fill=0)
                        draw.text((343, pos_name_p[i]), c[i][3], font=fnt, fill=0)
                        draw.text((343, pos_prepod[i]), par_all[0][c[i][1]-1], font=fnt, fill=0)
                    else:
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 30)
                        draw.text((20, pos_num_p[i]), str(c[i][1]), font=fnt, fill=0)
                        fnt = ImageFont.truetype(dirr + "6622.ttf", 14)
                        draw.text((53, pos_name_p[i]), c[i][2], font=fnt, fill=0)
                        draw.text((53, pos_prepod[i]), c[i][0], font=fnt, fill=0)
                        draw.text((343, pos_name_p[i]), c[i][3], font=fnt, fill=0)
                        draw.text((343, pos_prepod[i]), par_all[1][c[i][1]-1], font=fnt, fill=0)
        buf = BytesIO()
        img.save(buf, 'png')
        buf.seek(0)
        image_bytes = buf.read()
        buf.close()
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages(BytesIO(image_bytes))
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        vk.messages.send(
          user_id=int(event_user_id),
          random_id=get_random_id(),
          message=title,
          attachment=attachment)
    else:
        if week != 1:
            vk.messages.send(
              user_id=int(event_user_id),
              random_id=get_random_id(),
              message=title + '\nРасписание недоступно')

def message_n(user_, year, Bmon, mes, t_us, event_user_id, week):
    mes_end = d_all[mday_end][int(time.strftime('%m'))]
    m = ''
    date = datetime.date(year, Bmon, mes)
    timetup = date.timetuple()
    title = str(mes) + B_all[Bmon] + ' ' + week_all[int(time.strftime('%w', timetup))]
    c = execute_read_query('SELECT * FROM raspisanie WHERE ' + t_us + ' = "' + str(user_) + '" AND date_r = "' + str(mes) + B_all[Bmon] + '" ORDER BY number_par')
    
    if c != []:
        if t_us == 'groupa':
            date = datetime.date(year, Bmon, mes)
            timetup = date.timetuple()
            m = str(mes) + B_all[Bmon] + ' ' + week_all[int(time.strftime('%w', timetup))] + '\n' + c[0][0].replace('_', '-') + '\n'
            for i in range(0, len(c)):
                if c[i][2] != '':
                    if time.strftime('%w', timetup) != '6':
                        m = m + '\n' + str(c[i][1]) + " " + c[i][2] + " " + c[i][3]
                        m = m + '\n' + c[i][4] + '\n' + par_all[0][c[i][1] - 1] + '\n'
                    else:
                        m = m + '\n' + str(c[i][1]) + " " + c[i][2] + " " + c[i][3]
                        m = m + '\n' + c[i][4] + '\n' + par_all[1][c[i][1] - 1] + '\n'
        elif t_us == 'auditorium':
            date = datetime.date(year, Bmon, mes)
            timetup = date.timetuple()
            m = str(mes) + B_all[Bmon] + ' ' + week_all[int(time.strftime('%w', timetup))] + '\n' + c[0][3] + ' аудитория\n'
            for i in range(0, len(c)):
                if c[i][2] != '':
                    if time.strftime('%w', timetup) != '6':
                        m = m + '\n' + str(c[i][1]) + " " + c[i][2] + " " + c[i][0]
                        m = m + '\n' + c[i][4] + '\n' + par_all[0][c[i][1] - 1] + '\n'
                    else:
                        m = m + '\n' + str(c[i][1]) + " " + c[i][2] + " " + c[i][0]
                        m = m + '\n' + c[i][4] + '\n' + par_all[1][c[i][1] - 1] + '\n'
        elif t_us == 'Teacher':
            date = datetime.date(year, Bmon, mes)
            timetup = date.timetuple()
            m = str(mes) + B_all[Bmon] + ' ' + week_all[int(time.strftime('%w', timetup))] + '\n' + c[0][4] + '\n'
            for i in range(0, len(c)):
                if c[i][2] != '':
                    if time.strftime('%w', timetup) != '6':
                        m = m + '\n' + str(c[i][1]) + " " + c[i][2] + " " + c[i][3]
                        m = m + '\n' + c[i][0] + '\n' + par_all[0][c[i][1] - 1] + '\n'
                    else:
                        m = m + '\n' + str(c[i][1]) + " " + c[i][2] + " " + c[i][3]
                        m = m + '\n' + c[i][0] + '\n' + par_all[1][c[i][1] - 1] + '\n'
        vk.messages.send(
          user_id=int(event_user_id),
          random_id=get_random_id(),
          message=m)
    else:
        if week != 1:
            vk.messages.send(
              user_id=int(event_user_id),
              random_id=get_random_id(),
              message=title + '\nРасписание недоступно')

def ev_mess_new(event_text, event_user_id):
    user = str(event_user_id)
    
    text_mes_d = []
    
    mday_end = 0
    if int(time.strftime('%Y')) % 4 == 0:
        mday_end = 1
    year = int(time.strftime('%Y'))
    mes_all = []
    if int(time.strftime('%d')) + 7 > d_all[mday_end][int(time.strftime('%m'))]:
        for i in range(int(time.strftime('%d')), d_all[mday_end][int(time.strftime('%m'))] + 1):
            mes_all.append(i)
        mes_end = (int(time.strftime('%d')) + 7) - d_all[mday_end][int(time.strftime('%m'))]
        for i in range(1, mes_end):
            mes_all.append(i)
    else:
        for i in range(int(time.strftime('%d')), int(time.strftime('%d')) + 7):
            mes_all.append(i)
    for mes in range(0, 13):
        for day in range(1, d_all[mday_end][mes] + 1):
            text_mes_d.append(str(day) + B_all[mes].upper())

    if event_text.upper() == 'НАЧАТЬ' or event_text.upper() == '!РАСПИСАНИЕ' or event_text.upper() == 'START' or event_text.upper() == 'РАСПИСАНИЕ':
        Bmon = int(time.strftime('%m'))
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='https://vk.com/@-191083341-kak-polzovatsya-botom',
            keyboard=user_user.get_keyboard()
        )
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Расписание для',
            keyboard=user_user.get_keyboard()
        )
    elif event_text.upper() == 'ERROR' or event_text.upper() == 'ОШИБКА':
        user_name = vk_session.method("users.get", {"user_ids": event_user_id})
        fullname = user_name[0]['first_name'] +  ' ' + user_name[0]['last_name']
        rand = random.randint(0, 3)
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            sticker_id=stickers_id[rand]
        )
        vk.messages.send(
            user_id=201405354,
            random_id=get_random_id(),
            message=fullname + ", кажется, обнаружил(а) ошибку!"
        )
    elif groups.count(event_text.upper().replace(" ", "")) != 0:
        Bmon = int(time.strftime('%m'))
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user + ';')
        if fot_r != []:
            if fot_r[0][0] == 'true':
                data = VkKeyboard(one_time=False)
                data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
                data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Изображение \U0001F5BC', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
                data.add_line()
                data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
            else:
                data = VkKeyboard(one_time=False)
                data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
                data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
                data.add_line()
                data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        else:
            data = VkKeyboard(one_time=False)
            data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
            data.add_line()
            data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
            data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
            data.add_line()
            data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
            data.add_line()
            data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Введите день',
            keyboard=data.get_keyboard()
        )
        try:
            fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user + ';')
            execute_query('DELETE FROM students WHERE id = ' + user + ';')
            execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + event_text.upper().replace(" ", "") + '", "' + fot_r[0][0] + '")' + ';')
        except:
            execute_query('DELETE FROM students WHERE id = ' + user + ';')
            execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + event_text.upper().replace(" ", "") + '", "' + 'false' + '")' + ';')
    elif auditoriums.count(event_text) != 0:
        Bmon = int(time.strftime('%m'))
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user + ';')
        if fot_r != []:
            if fot_r[0][0] == 'true':
                data = VkKeyboard(one_time=False)
                data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
                data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Изображение \U0001F5BC', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
                data.add_line()
                data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
            else:
                data = VkKeyboard(one_time=False)
                data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
                data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
                data.add_line()
                data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        else:
            data = VkKeyboard(one_time=False)
            data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
            data.add_line()
            data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
            data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
            data.add_line()
            data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
            data.add_line()
            data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Введите день',
            keyboard=data.get_keyboard()
        )
        try:
            fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user + ';')
            execute_query('DELETE FROM students WHERE id = ' + user + ';')
            execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + event_text + '", "' + fot_r[0][0] + '")' + ';')
        except:
            execute_query('DELETE FROM students WHERE id = ' + user + ';')
            execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + event_text + '", "' + 'false' + '")' + ';')
    elif Teachers.count(event_text) != 0:
        Bmon = int(time.strftime('%m'))
        try:
            fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user + ';')
            execute_query('UPDATE students SET foto_r = "' + fot_r[0][0] + '" WHERE id = ' + user + ';')
        except:
            execute_query('UPDATE students SET foto_r = "false" WHERE id = ' + user + ';')
        if fot_r != []:
            if fot_r[0][0] == 'true':
                data = VkKeyboard(one_time=False)
                data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
                data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Изображение \U0001F5BC', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
                data.add_line()
                data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
            else:
                data = VkKeyboard(one_time=False)
                data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
                data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
                data.add_line()
                data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
                data.add_line()
                data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        else:
            data = VkKeyboard(one_time=False)
            data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
            data.add_line()
            data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
            data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
            data.add_line()
            data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
            data.add_line()
            data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Введите день',
            keyboard=data.get_keyboard()
        )
        try:
            fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user + ';')
            execute_query('DELETE FROM students WHERE id = ' + user + ';')
            execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + event_text + '", "' + fot_r[0][0] + '")' + ';')
        except:
            execute_query('DELETE FROM students WHERE id = ' + user + ';')
            execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + event_text + '", "' + 'false' + '")' + ';')
    elif event_text.upper() == 'СТУДЕНТ':
        c = []
        c += execute_read_query('SELECT groupa FROM activ ORDER BY number_ DESC')
        keyboard1 = VkKeyboard(one_time=False)
        keyboard1.add_button(c[0][0], color=VkKeyboardColor.PRIMARY)
        keyboard1.add_line()
        keyboard1.add_button(c[1][0], color=VkKeyboardColor.PRIMARY)
        keyboard1.add_line()
        keyboard1.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Введите группу',
            keyboard=keyboard1.get_keyboard()
        )
    elif event_text.upper() == 'ПРЕПОДАВАТЕЛЬ':
        user_name = vk_session.method("users.get", {"user_ids": event_user_id})
        fam = user_name[0]['last_name']
        nam = user_name[0]['first_name']
        newlist = []
        c = []
        c += execute_read_query('SELECT Teacher FROM raspisanie WHERE Teacher LIKE "%' + fam + " " + nam[0] + '.%" GROUP BY Teacher')
        c += execute_read_query('SELECT Teacher FROM raspisanie WHERE Teacher LIKE "%' + fam + '%" GROUP BY Teacher')
        c += execute_read_query('SELECT Teacher FROM raspisanie WHERE Teacher LIKE "% ' + nam[0] + '.%" GROUP BY Teacher')
        for i in c:
            if i[0] not in newlist:
                newlist.append(i[0])
        if len(newlist) < 2:
            tea = {}
            tea = execute_read_query('SELECT Teacher FROM raspisanie GROUP BY Teacher')
            for i in range(0, 2 - len(newlist)):
                rand2 = random.randint(0, len(tea) - 1)
                newlist += tea[rand2]
        keyboard2 = VkKeyboard(one_time=False)
        keyboard2.add_button(newlist[0], color=VkKeyboardColor.PRIMARY)
        keyboard2.add_line()
        keyboard2.add_button(newlist[1], color=VkKeyboardColor.PRIMARY)
        keyboard2.add_line()
        keyboard2.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Введите преподавателя',
            keyboard=keyboard2.get_keyboard()
        )
    elif event_text.upper() == 'АУДИТОРИЯ':
        rand3 = random.randint(0, len(auditoriums) - 2)
        keyboard3 = VkKeyboard(one_time=False)
        keyboard3.add_button(auditoriums[rand3], color=VkKeyboardColor.PRIMARY)
        keyboard3.add_line()
        keyboard3.add_button(auditoriums[rand3 + 1], color=VkKeyboardColor.PRIMARY)
        keyboard3.add_line()
        keyboard3.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Введите аудиторию',
            keyboard=keyboard3.get_keyboard()
        )
    elif event_text.upper() == 'РАСПИСАНИЕ НА НЕДЕЛЮ' or event_text == 'Расписание на неделю \U0001F5D3':
        year = int(time.strftime('%Y'))
        Bmon = int(time.strftime('%m'))
        Bmon_a = []
        fot_r = []
        mes_all = []
        if int(time.strftime('%d')) + 7 > d_all[mday_end][int(time.strftime('%m'))]:
            for i in range(int(time.strftime('%d')), d_all[mday_end][int(time.strftime('%m'))] + 1):
                mes_all.append(i)
                Bmon_a.append(Bmon)
            mes_end = (int(time.strftime('%d')) + 7) - d_all[mday_end][int(time.strftime('%m'))]
            for i in range(1, mes_end):
                mes_all.append(i)
                Bmon_a.append(Bmon + 1)
        else:
            for i in range(int(time.strftime('%d')), int(time.strftime('%d')) + 7):
                mes_all.append(i)
                Bmon_a.append(Bmon)
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        for i in range(0, len(mes_all)):
            if fot_r[0][0] == 'true':
                if groups.count(user_group[0][0]) != 0:
                    message_pic(user_group[0][0], year, Bmon_a[i], mes_all[i], "groupa", user, 1)
                    Bmon = int(time.strftime('%m'))
                elif auditoriums.count(str(user_group[0][0])) != 0:
                    message_pic(user_group[0][0], year, Bmon_a[i], mes_all[i], "auditorium", user, 1)
                    Bmon = int(time.strftime('%m'))
                elif Teachers.count(user_group[0][0]) != 0:
                    message_pic(user_group[0][0], year, Bmon_a[i], mes_all[i], "Teacher", user, 1)
                    Bmon = int(time.strftime('%m'))
            else:
                if groups.count(user_group[0][0]) != 0:
                    message_n(user_group[0][0], year, Bmon_a[i], mes_all[i], "groupa", user, 1)
                    Bmon = int(time.strftime('%m'))
                elif auditoriums.count(str(user_group[0][0])) != 0:
                    message_n(user_group[0][0], year, Bmon_a[i], mes_all[i], "auditorium", user, 1)
                    Bmon = int(time.strftime('%m'))
                elif Teachers.count(user_group[0][0]) != 0:
                    message_n(user_group[0][0], year, Bmon_a[i], mes_all[i], "Teacher", user, 1)
                    Bmon = int(time.strftime('%m'))
    elif event_text.upper() == 'ЗАВТРА' or event_text == 'Завтра \U0001F4C6':
        year = int(time.strftime('%Y'))
        Bmon = int(time.strftime('%m'))
        fot_r = []
        mes = int(time.strftime('%d'))
        mes_end = d_all[mday_end][int(time.strftime('%m'))]
        if mes == mes_end:
            mes = 1
            if Bmon == 12:
                Bmon = 1
            else:
                Bmon = Bmon + 1
        else:
            mes = mes + 1
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        if fot_r[0][0] == 'true':
            if groups.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
        else:
            if groups.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
    elif event_text.upper() == 'СЕГОДНЯ' or event_text == 'Сегодня \U0001F4C5':
        year = int(time.strftime('%Y'))
        Bmon = int(time.strftime('%m'))
        fot_r = []
        mes = int(time.strftime('%d'))
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        if fot_r[0][0] == 'true':
            if groups.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
        else:
            if groups.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
    elif event_text.upper() == 'ОТМЕНА' or event_text == 'Отмена \U0001F519':
        Bmon = int(time.strftime('%m'))
        execute_query('DELETE FROM students WHERE id = ' + user + ';')
        vk.messages.send(
            user_id=event_user_id,
            random_id=get_random_id(),
            message='Расписание для',
            keyboard=user_user.get_keyboard()
        )
    elif dd_all.count(event_text) != 0:
        year = int(time.strftime('%Y'))
        Bmon = int(time.strftime('%m'))
        fot_r = []
        mes = int(event_text)
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        if fot_r[0][0] == 'true':
            if groups.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
        else:
            if groups.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
    elif text_mes_d.count(event_text.upper()) != 0:
        year = int(time.strftime('%Y'))
        fot_r = []
        for mmsec in range(0, 13):
            if event_text.upper().split(' ')[1] == B_all[mmsec].replace(' ', '').upper():
                Bmon = int(mmsec)
        mes = int(event_text.split(' ')[0])
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        if fot_r[0][0] == 'true':
            if groups.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
        else:
            if groups.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "groupa", user, 0)
                Bmon = int(time.strftime('%m'))
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "auditorium", user, 0)
                Bmon = int(time.strftime('%m'))
            elif Teachers.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], year, Bmon, mes, "Teacher", user, 0)
                Bmon = int(time.strftime('%m'))
    elif re.search('\d\d.\d\d', event_text):
        date_full = re.search('\d\d.\d\d', event_text)[0].split('.')
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        if fot_r[0][0] == 'true':
            if groups.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "groupa", user, 0)
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_pic(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "auditorium", user, 0)
            elif Teachers.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "Teacher", user, 0)
        else:
            if groups.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "groupa", user, 0)
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_n(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "auditorium", user, 0)
            elif Teachers.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "Teacher", user, 0)
    elif event_text.upper() == '/PICTURE' or event_text == 'Текст \U0001F4C3':
        execute_query('UPDATE students SET foto_r = "true" WHERE id = ' + user)
        data = VkKeyboard(one_time=False)
        data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
        data.add_line()
        data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
        data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
        data.add_line()
        data.add_button('Изображение \U0001F5BC', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
        data.add_line()
        data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
           user_id=event_user_id,
           random_id=get_random_id(),
           message="Вы успешно переключились на режим отображения расписания изображением.",
           keyboard=data.get_keyboard())
    elif event_text.upper() == '/TEXT' or event_text == 'Изображение \U0001F5BC':
        execute_query('UPDATE students SET foto_r = "false" WHERE id = ' + user)
        data = VkKeyboard(one_time=False)
        data.add_button("Расписание на неделю \U0001F5D3", color=VkKeyboardColor.PRIMARY)
        data.add_line()
        data.add_button('Сегодня \U0001F4C5', color=VkKeyboardColor.PRIMARY)
        data.add_button('Завтра \U0001F4C6', color=VkKeyboardColor.PRIMARY)
        data.add_line()
        data.add_button('Текст \U0001F4C3', color=VkKeyboardColor.PRIMARY) # U0001F4C3, U0001F5BC
        data.add_line()
        data.add_button('Отмена \U0001F519', color=VkKeyboardColor.SECONDARY) #SECONDARY, DEFAULT
        vk.messages.send(
           user_id=event_user_id,
           random_id=get_random_id(),
           message="Вы успешно переключились на режим отображения расписания текстом.",
           keyboard=data.get_keyboard())
    elif event_text == '/reset':
        if user == '201405354':
            execute_query('UPDATE activ SET number_ = 0')
            vk.messages.send(
               user_id=event_user_id,
               random_id=get_random_id(),
               message="OK")
        else:
            vk.messages.send(
               user_id=event_user_id,
               random_id=get_random_id(),
               message="Ты не админ")
    elif event_text.upper() == '/TOP':
        top = execute_read_query('SELECT groupa FROM activ ORDER BY number_ DESC')
        spisok = ''
        top3 = ['\U0001F947', '\U0001F948', '\U0001F949', '', '', '', '', '', '', '']
        for x in range(10):
            koo = execute_read_query('SELECT number_ FROM activ WHERE groupa = "' + str(top[x][0]) + '";')
            spisok = spisok + str(x + 1) + '. ' + top3[x] + str(top[x][0]) + ': ' + str(koo[0][0]) + '\n'
        vk.messages.send(
           user_id=event_user_id,
           random_id=get_random_id(),
           message=spisok
       )
    elif week_all_u.count(event_text.upper()) != 0:
        wii = 0
        user_group = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
        for wday in week_all_u:
            wii = wii + 1
            if wday == event_text.upper():
                c = execute_read_query('SELECT date_r FROM raspisanie WHERE date_r LIKE "% ' + week_all[wii] + '" AND groupa = "' + user_group[0][0] + '"')
        fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
        if fot_r[0][0] == 'true':
            if groups.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "groupa", user, 0)
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_pic(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "auditorium", user, 0)
            elif Teachers.count(user_group[0][0]) != 0:
                message_pic(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "Teacher", user, 0)
        else:
            if groups.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "groupa", user, 0)
            elif auditoriums.count(str(user_group[0][0])) != 0:
                message_n(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "auditorium", user, 0)
            elif Teachers.count(user_group[0][0]) != 0:
                message_n(user_group[0][0], int(time.strftime('%Y')), int(date_full[1]), int(date_full[0]), "Teacher", user, 0)
    else:
        c = []
        # SELECT Teacher FROM raspisanie WHERE Teacher LIKE "%Руденко%" GROUP BY Teacher
        c += execute_read_query('SELECT Teacher FROM raspisanie WHERE Teacher LIKE "%' + event_text + '%" GROUP BY Teacher')
        c += execute_read_query('SELECT auditorium FROM raspisanie WHERE auditorium LIKE "%' + event_text + '%" GROUP BY auditorium')
        keyboard_1 = VkKeyboard(one_time=False, inline=True)
        for g in groups:
            if event_text.upper().replace('-', '').replace(' ', '') == g.replace('-', '').replace(' ', ''):
                messag = "Возможно вы имели в виду:"
                keyboard_1.add_button(g, color=VkKeyboardColor.PRIMARY)
                keyboard_1.add_line()
                vk.messages.send(
                   user_id=event_user_id,
                   random_id=get_random_id(),
                   message=messag,
                   keyboard=keyboard_1.get_keyboard())
        c += execute_read_query('SELECT groupa FROM raspisanie WHERE groupa LIKE "%' + event_text.upper() + '%" GROUP BY groupa')
        messag = "Возможно вы имели в виду:\n"
        for i in c[:5]:
            keyboard_1.add_button(i[0], color=VkKeyboardColor.PRIMARY)
            keyboard_1.add_line()
            messag += i[0] + '\n'
        if messag != "Возможно вы имели в виду:\n":
            vk.messages.send(
               user_id=event_user_id,
               random_id=get_random_id(),
               message=messag,
               keyboard=keyboard_1.get_keyboard())
        else:
            vk.messages.send(
               user_id=event_user_id,
               random_id=get_random_id(),
               message=messag,
               keyboard=keyboard_1.get_keyboard())

@app.route('/c4d63d1bcaa1e7b7da4ee637ead47256', methods=['POST'])
def bot():
    top_groupa_1 = "18ПКС"
    epoch_time = int(time.time())
    # for event_n in vk.messages.getConversations(filter='unanswered')['items']:
    #     try:
    #         ev_mess_new(event_n['last_message']['text'], event_n['last_message']['from_id'])
    #     except:
    #         pass
    data = request.get_json(force=True, silent=True)
    if not data or data['secret'] != 'imvb2vcdij8':
        return 'not ok'
    if data['type'] == 'confirmation':
        return confirmation_code
    elif data['type'] == 'message_new' and data['object']['message']['peer_id'] == data['object']['message']['from_id'] and int(data['object']['message']['date']) > epoch_time - 10:
        try:
            user = str(data['object']['message']['peer_id'])
            c = execute_read_query('SELECT groupa FROM students WHERE id = ' + user)
            fot_r = execute_read_query('SELECT foto_r FROM students WHERE id = ' + user)
            if fot_r != []:
                execute_query('INSERT INTO students (id, groupa, foto_r) VALUES (' + user + ', "' + c[0][0] + '", "' + fot_r[0][0] + '")')
            if c != []:
                try:
                    if groups.count(c[0][0]) != 0:
                        g = execute_read_query('SELECT number_ FROM activ WHERE groupa = "' + c[0][0] + '"')
                        execute_query('UPDATE activ SET number_ = "' + str(g[0][0] + 1) + '" WHERE groupa = "' + c[0][0] + '"')
                        top_groupa = "18ПКС"
                        c = execute_read_query("SELECT groupa FROM activ ORDER BY number_ DESC")
                        top_groupa = c[0][0]
                        if top_groupa != top_groupa_1:
                            top_groupa_1 = top_groupa
                            subprocess.Popen(['python3', dirr + 'top_groupa.py', top_groupa])
                except IndexError:
                    pass
            ev_mess_new(data['object']['message']['text'], user)
        except:
            log.exception(traceback.format_exc())
        return 'ok'

    return 'ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
