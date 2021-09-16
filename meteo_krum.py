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


def is_int(val):
    try:
        if type(int(val)) == int:
            return True
        else:
            if val.is_integer():
                return True
            else:
                return False
    except:
        return False


pat = re.compile(r'\d{4}')


def count_messages(messages):
    result = []
    for message in messages:
        date1 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {message[0][8:10]}:{message[0][10:12]}'
        date2 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {re.findall(pat, message[3])[0][0:2]}:{re.findall(pat, message[3])[0][2:4]}'
        first_time = datetime.strptime(date1, '%Y/%m/%d %H:%M')
        second_time = datetime.strptime(date2, '%Y/%m/%d %H:%M')
        delta = timedelta(minutes=1)
        if abs(first_time - second_time) > delta and date1[11:] != '00:00' and date2[11:] != '23:59':
            result.append(message)
            errors.append(abs(first_time - second_time))
        if date1[11:] == '00:00' and date2[11:] != '23:59' and date2[11:] != '00:00':
            result.append(message)
    return result


def count_messages2(messages):
    result = []
    for message in messages:
        date1 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {message[0][8:10]}:{message[0][10:12]}'
        date2 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {re.findall(pat, message[4])[0][0:2]}:{re.findall(pat, message[4])[0][2:4]}'
        first_time = datetime.strptime(date1, '%Y/%m/%d %H:%M')
        second_time = datetime.strptime(date2, '%Y/%m/%d %H:%M')
        delta = timedelta(minutes=1)
        if abs(first_time - second_time) > delta and date1[11:] != '00:00' and date2[11:] != '23:59':
            result.append(message)
            errors.append(abs(first_time - second_time))
        if date1[11:] == '00:00' and date2[11:] != '23:59' and date2[11:] != '00:00':
            result.append(message)
    return result


def count_messages3(messages):
    result = []
    for message in messages:
        date1 = f'{message[1][0:4]}/{message[1][4:6]}/{message[1][6:8]} {message[1][8:10]}:{message[1][10:12]}'
        date2 = f'{message[1][0:4]}/{message[1][4:6]}/{message[1][6:8]} {re.findall(pat, message[4])[0][0:2]}:{re.findall(pat, message[4])[0][2:4]}'
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
    correct_messages2 = []
    correct_messages3 = []
    for item in parts_message:
        if len(item) >= 3:
            if item[2][0:2] == '03' and len(item[0]) > 10:
                date = f'{item[0][0:4]}/{item[0][4:6]}/{item[0][6:8]} {item[0][8:10]}:{item[0][10:12]}:{item[0][12:14]}'
                time = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                if date_begin <= time <= date_end:
                    correct_messages.append(item)
            if len(item) >= 5:
                if item[3][0:2] == '03' and len(item[0]) > 10 and is_int(item[0][0:10]) is True:
                    date = f'{item[0][0:4]}/{item[0][4:6]}/{item[0][6:8]} {item[0][8:10]}:{item[0][10:12]}:{item[0][12:14]}'
                    time = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                    if date_begin <= time <= date_end:
                        correct_messages2.append(item)
            if len(item) >= 4:
                if item[3][0:2] == '03' and len(item[1]) > 10 and is_int(item[1][0:10]) is True:
                    date = f'{item[1][0:4]}/{item[1][4:6]}/{item[1][6:8]} {item[1][8:10]}:{item[1][10:12]}:{item[1][12:14]}'
                    time = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                    if date_begin <= time <= date_end:
                        correct_messages3.append(item)
    result1 = count_messages(correct_messages)
    result2 = count_messages2(correct_messages2)
    result3 = count_messages3(correct_messages3)
    result = result1 + result2 + result3
    lst.append(file)
    lst.append(result)
    result_file.append(lst)

if not os.path.exists('result_KRUM'):
    os.makedirs('result_KRUM')

for item in result_file:
    name = item[0]
    if item[1]:
        with open(f'result_KRUM/ERROR_{name}', 'w') as output:
            output.write('NAME OF FILE: ' + name + '\n\n')
            for lst in item[1]:
                for string in lst:
                    output.write(string + '\n')
                output.write('NNNN\n\n')

print('Скрипт завершен')

# max_error = max(errors)
# min_error = min(errors)
# mod_error = max(set(errors), key=errors.count)
# print(f'Максимальная ошибка составила {max_error},\n'
#       f'Минимальная ошибка составила {min_error},\n'
#       f'Самая часто встречающаяся ошибка {mod_error}')
