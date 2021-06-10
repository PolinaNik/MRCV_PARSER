import os
import itertools
from datetime import datetime
from datetime import timedelta

list_of_files = os.listdir('files')
result_file = []

def count_messages(messages):
    result = []
    for message in messages:
        date1 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {message[0][8:10]}:{message[0][10:12]}'
        date2 = f'{message[0][0:4]}/{message[0][4:6]}/{message[0][6:8]} {message[3][9:11]}:{message[3][11:13]}'
        first_time = datetime.strptime(date1, '%Y/%m/%d %H:%M')
        second_time = datetime.strptime(date2, '%Y/%m/%d %H:%M')
        delta = timedelta(minutes=1)
        if abs(first_time - second_time) > delta and date1[11:] != '00:00' and date2[11:] != '23:59':
            result.append(message)
            print(date1)
            print(date2)
        if date1[11:] == '00:00' and date2[11:] != '23:59' and date2[11:] != '00:00':
            result.append(message)
    return result


for file in list_of_files:
    lst = []
    print(file)
    f = open(f'files/{file}', 'r', encoding='utf-8', errors='ignore')
    mrcv_log = f.readlines()
    saparator = 'NNNN\n'
    all_messages = [list(y) for x, y in itertools.groupby(mrcv_log, lambda z: z == saparator) if not x]
    messages_03 = [item for item in all_messages if item[2][0:2] == '03']
    result = count_messages(messages_03)
    lst.append(file)
    lst.append(result)
    result_file.append(lst)

if not os.path.exists('result'):
    os.makedirs('result')

for item in result_file:
    name = item[0]
    if item[1]:
        with open(f'result/ERROR_{name}', 'w') as output:
            output.write('NAME OF FILE: '+name+'\n\n')
            for lst in item[1]:
                for string in lst:
                    new = ''.join(string)
                    output.write(new)
                output.write('NNNN\n')

# with open('mrcv-20210414_010026.log', 'r', encoding='utf-8', errors='ignore') as file:
#     mrcv_log = file.readlines()
#
#
# saparator = 'NNNN\n'
#
# all_messages = [list(y) for x, y in itertools.groupby(mrcv_log, lambda z: z == saparator) if not x]
#
# messages_03 = [item for item in all_messages if item[2][0:2] == '03']
#
#
# result = count_messages(messages_03)


