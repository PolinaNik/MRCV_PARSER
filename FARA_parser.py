import os
from datetime import datetime
from datetime import timedelta

list_of_files = os.listdir('files')
result_file = []
errors = []

date_begin = datetime.fromisoformat('2021-09-08T22:30:00')
date_end = datetime.fromisoformat('2021-09-09T00:30:00')

# time1 = f'{item[0][0:4]}/{item[0][4:6]}/{item[0][6:8]} {item[0][8:10]}:{item[0][10:12]}:{item[0][12:14]}'
#             try:
#                 time = datetime.strptime(time1, '%Y/%m/%d %H:%M:%S')


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

for x in correct_items:
    print(x)
