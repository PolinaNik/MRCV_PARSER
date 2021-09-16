import os
from datetime import datetime
from datetime import timedelta
import sys

list_of_files = os.listdir('files')
result_file = []
errors = []

d1 = input('Введите дату и время начала в формате ГГГГ-ММ-ДД чч:мм:сс: ')
d2 = input('Введите дату и время конца в формате ГГГГ-ММ-ДД чч:мм:сс: ')

try:
    y1 = d1.split(' ')[0]
    t1 = d1.split(' ')[1]
    date_begin = datetime.fromisoformat(f'{y1}T{t1}')
except:
    print('Неверный формат даты начала')
    sys.exit()

try:
    y2 = d2.split(' ')[0]
    t2 = d2.split(' ')[1]
    date_end = datetime.fromisoformat(f'{y2}T{t2}')
except:
    print('Неверный формат даты конца')
    sys.exit()

for file in list_of_files:
    lst = []
    f = open(f'files/{file}', 'r', encoding='utf-8', errors='ignore')
    mrcv_log = f.read()
    all_items = mrcv_log.split('NNNN')
    parts_item = [list(filter(None, x.split('\n'))) for x in all_items]
    correct_items = []
    for item in parts_item:
        if len(item) >= 3:
            if item[2][0:2] == '16' and len(item[0]) > 10:
                if item[3][0:4] == 'FARA':
                    date = f'{item[0][0:4]}/{item[0][4:6]}/{item[0][6:8]} {item[0][8:10]}:{item[0][10:12]}:{item[0][12:14]}'
                    time = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                    if time >= date_begin:
                        correct_items.append(item)
            if len(item) >= 4:
                if item[3][0:2] == '16' and item[4][0:4] == 'FARA':
                    date = f'{item[0][0:4]}/{item[0][4:6]}/{item[0][6:8]} {item[0][8:10]}:{item[0][10:12]}:{item[0][12:14]}'
                    time = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                    if time >= date_begin:
                        correct_items.append(item)

print('Найдены следующие сообщения FARA за указанный период:')
for x in correct_items:
    print(x)
