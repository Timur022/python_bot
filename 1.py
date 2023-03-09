from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook
from io import BytesIO
import datetime
import time
import mysql.connector
from mysql.connector import Error
import asyncio
import logging
import traceback
import json


# dirr = ""
dirr = "/home/rasptest/"

logging.basicConfig(filename= dirr + "pars.log", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
log = logging.getLogger("ex")

B_all = [" ", " Января", " Февраля", " Марта", " Апреля", " Мая", " Июня", " Июля", " Августа", " Сентября", " Октября", " Ноября", " Декабря"]
nomer = ['1', '2', '3', '4', '5', '6', '7']
m_all = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12]
d_all = [[0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
         [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

mday_end = 0

if int(time.strftime('%Y')) % 4 == 0:
    mday_end = 1
day_par = {}

groups_group = []

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
    connection = create_connection("localhost", "root", "пароль", "rasp")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def execute_read_query(query):
    connection = create_connection("localhost", "root", "пароль", "rasp")
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


# conn = sqlite3.connect("rasp.db")
# with conn:
#     cur = conn.cursor()
#     cur.execute("SELECT groupa FROM raspis GROUP BY groupa")
#     gr0 = cur.fetchall()
# for i in gr0:
#     groups_group.append(i[0])
#     

gr0 = execute_read_query("SELECT groupa FROM activ")
for i in gr0:
    groups_group.append(i[0])

mess = int(time.strftime('%d'))
Bmon = int(time.strftime('%m'))
year = int(time.strftime('%Y'))
date = datetime.date(year, Bmon, mess)
timetup = date.timetuple()
days = []
month = []

mday_end = 0

while True:
    try:
        if time.strftime('%X') == '00:00:00' and time.strftime('%w', timetup) == '0':
            execute_query("UPDATE activ SET number_ = 0")
        elif time.strftime('%X') == '12:00:00' or time.strftime('%X') == '23:00:00' and int(requests.get("https://www.uc.osu.ru/").status_code) == 200:
            mess = int(time.strftime('%d'))
            Bmon = int(time.strftime('%m'))
            year = int(time.strftime('%Y'))
            date = datetime.date(year, Bmon, mess)
            timetup = date.timetuple()
            days = []
            month = []

            mday_end = 0
# postman
            if int(time.strftime('%Y')) % 4 == 0:
                mday_end = 1
            if int(time.strftime('%d')) + 14 > d_all[mday_end][int(time.strftime('%m'))]:
                for i in range(int(time.strftime('%d')), d_all[mday_end][int(time.strftime('%m'))] + 1):
                    days.append(str(i))
                    month.append(m_all[Bmon])
                end = (int(time.strftime('%d')) + 14) - d_all[mday_end][int(time.strftime('%m'))]
                for i in range(1, end):
                    days.append(str(i))
                    month.append(m_all[Bmon + 1])
            else:
                for i in range(int(time.strftime('%d')), int(time.strftime('%d')) + 14):
                    days.append(str(i))
                    month.append(m_all[Bmon])
            # with open("text_group.txt", "r") as fp:
            #     for line in fp:
            #         groups_group.append(line.replace('\n', ''))
            execute_query('DROP TABLE raspisanie')
            query = 'CREATE TABLE raspisanie (groupa varchar(20), number_par int, discipline varchar(50), auditorium varchar(20), Teacher varchar(50), date_r varchar(20))'
            execute_query(query)
            # teachers_arr = ["Абузярова И.И.","Авдеева Т.П.","Адакаев Р.Р.","Атяскина Т.В.","Баскакова А.С.","Бегун А.С.","Беломестнова М.Р.","Бережко О.Ю.","Бородавкина Н.М.","Боярсков С.Г.","Бурма Т.П.","Бухтоярова А.А.","Бушуй Л.А.","Варламова Е.Ю.","Воякина Е.В.","Галкина А.В.","Гапоненко А.В.","Германова К.В.","Горышева Т.С.","Грекова Л.А.","Гурьянов А.А.","ГусейноваТ.Н.","Давлятмуродов Г.Х.","Дегтярева Л.А.","Егоренко Н.В.","Егорова В.Н.","Епифанова Е.А.","Есипов Ю.В.","Жданов В.А.","Зобина Ю.В.","Зотова А.В.","Исмагилова Л.А.","Калинина И.А.","Канивец Е.К.","Капустин А.В.","Каримова Ю.М.","Карсков А.Ю.","Касаткин С.М.","Кенжина Ю.А.","Колесник Е.А.","Колычева О.П.","Коптелова Е.Ю.","Костенко Н.Г.","Костин Д.В.","Кравцова О.С.","Кривошеева Н.А.","Кузнецова Н.Н.","Купарева Т.В.","Курмакаев Р.Р.","Кутищева Е.С.","ЛукеринаО.А.","Лысенко Е.О.","Максимычева М.П.","Малахова О.Б.","Малянова Л.Г.","Мангутов Ш.Р.","Манин А.Д.","Меженская М.С.","Мещерякова И.Н.","Недорезова Н.А.","Непоклонова Г.В.","Перехода М.А.","Першина Т.О.","Погорелова А.В.","Подоляк Н.Я.","Полывяная Л.А.","Припадчева Л.В.","Проданова О.С.","Рубцова О.С.","Руденко С.Н.","Русяев К.В.","Саитова С.И.","Салимова И.Х.","Самарцев С.В.","Свистунова Т.В.","Седова А.А.","Середа В.Ю.","Середа М.В.","Сидорова О.С.","Синицина А.Д.","Смольянов А.В.","Соколова В.А.","Степанов Д.С.","Счастьева Л.М.","Таспаева М.Г.","Тесля Н.В.","Уйманова Н.А.","Ушакова О.А.","Ханжин С.В.","Хасанова Е.А.","Химутина И.А.","Ходырева И.С.","Хромова О.Ю.","Чаплыгина Ю.В.","Чузов А.А.","Шамсутдинова С.А.","Шендерюк В.В.","Шигаева Е.А.","Шуринов И.А.","Щербаков А.Б.","Янбаева А.В.","Шатова В.А.","Шамсутдинов С.Н.","Степанчукова А.В.","Солтус Н.В.","Селиванова Л.А.","Русанова И.Ф.","Пузанов Н.В.","Плесовских А.Ю.","Панарина Е.А.","ОсиповаТ.О","Окшин Д.А.",]

            for d in range(0, len(days)):
                res0 = requests.post("https://www.uc.osu.ru/back_parametr.php", data={ 'type_id': 1, 'data' : '{0}-{1}-{2}'.format('0'+str(days[d]) if int(days[d]) < 10 else days[d], '0'+str(month[d]) if int(month[d]) < 10 else month[d], year)})
                if res0.text != '':
                    aDict = json.loads(res0.text)
                    for i in aDict.keys():
                        res = requests.post("https://www.uc.osu.ru/generate_data.php", data={ 'type': 1, 'data' : '{0}-{1}-{2}'.format('0'+str(days[d]) if int(days[d]) < 10 else days[d], '0'+str(month[d]) if int(month[d]) < 10 else month[d], year) , 'id' : i })
                        # print(res.text)
                        soup = BeautifulSoup(res.text, "html.parser")
                        all_rasp = soup.findAll('tr')
                        if all_rasp == []:
                            break
                        rasp = []
                        rasp_all = []
                        for ii in all_rasp:
                            str_rasp = ii.findAll('td')
                            for jj in str_rasp:
                                rasp.append(jj.text)
                            rasp_all.append(rasp)
                        rasp = []
                        l = len(rasp_all[0])
                        g = 0
                        for ii in range(3, l, 4):
                            execute_query('INSERT INTO raspisanie(groupa, number_par, discipline, auditorium, Teacher, date_r) VALUES("{0}", {1}, "{2}", "{3}", "{4}", "{5}")'.format(rasp_all[0][1], rasp_all[0][ii-1], rasp_all[0][ii], rasp_all[0][ii+1], rasp_all[0][ii+2], str(days[d]) + B_all[month[d]]))
    except:
        log.exception(traceback.format_exc())
