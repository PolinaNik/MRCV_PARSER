import os
from datetime import datetime
from datetime import timedelta
import re
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


def count_messages(messages):
    result = []
    pat = re.compile(r'\d+')
    for message in messages:
        date1 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {message[0][8:10]}:{message[0][10:12]}'
        info_date2 = re.findall(pat, message[3])[0]
        date2 = f'{message[0][0:4]}/{message[0][4:6]}/{info_date2[0:2]} {info_date2[2:4]}:{info_date2[4:6]}'
        first_time = datetime.strptime(date1, '%Y/%m/%d %H:%M')
        second_time = datetime.strptime(date2, '%Y/%m/%d %H:%M')
        delta = timedelta(minutes=1)
        if abs(first_time - second_time) > delta and date1[11:] != '00:00' and date2[11:] != '23:59':
            result.append(message)
            errors.append(abs(first_time - second_time))
        if date1[11:] == '00:00' and date2[11:] != '23:59' and date2[11:] != '00:00':
            result.append(message)
    return result


for file in list_of_files:
    lst = []
    f = open(f'files/{file}', 'r', encoding='utf-8', errors='ignore')
    mrcv_log = f.read()
    all_messages = mrcv_log.split('NNNN')
    parts_message = [list(filter(None, x.split('\n'))) for x in all_messages]
    correct_messages = []
    for item in parts_message:
        if len(item) >= 3:
            if item[2][0:2] == '04' and len(item[0]) > 10 and item[3][0:5] == 'METAR':
                date = f'{item[0][0:4]}/{item[0][4:6]}/{item[0][6:8]} {item[0][8:10]}:{item[0][10:12]}:{item[0][12:14]}'
                time = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                if date_begin <= time <= date_end:
                    correct_messages.append(item)
    result = count_messages(correct_messages)
    lst.append(file)
    lst.append(result)
    result_file.append(lst)

if not os.path.exists('result_METAR'):
    os.makedirs('result_METAR')

for item in result_file:
    name = item[0]
    if item[1]:
        with open(f'result_METAR/ERROR_{name}', 'w') as output:
            output.write('NAME OF FILE: '+name+'\n\n')
            for lst in item[1]:
                for string in lst:
                    output.write(string+'\n')
                output.write('NNNN\n\n')


max_error = max(errors)
min_error = min(errors)
mod_error = max(set(errors), key=errors.count)
print(f'Максимальная ошибка составила {max_error},\n'
      f'Минимальная ошибка составила {min_error},\n'
      f'Самая часто встречающаяся ошибка {mod_error}')

print('Скрипт завершен')