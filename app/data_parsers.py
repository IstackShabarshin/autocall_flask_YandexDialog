#!/usr/bin/env python
# coding: utf-8

# In[23]:


###-----------------------------------------------------------------------------
### Инициализация библиотек
###-----------------------------------------------------------------------------

import pandas as pd # для работы с файлами
from app.NatashaParser import (
    FindNames, # поиск имен в сообщений
    SplitOnSegments, # для разбиения на токены сообщений
    Normalize # для приведения к инфинитиву
)

# Игнорируем предупреждения о типах в pandas (проблемы pandas)
import warnings
warnings.filterwarnings('ignore')


###-----------------------------------------------------------------------------
### Константы таблиц
###-----------------------------------------------------------------------------


ADDRESS_STACK = 'app/data/UsersStacks.json' # стек состояний #TODO address -> dir
ADDRESS_DEPARTMENTS_FULL = 'app/data/Departments.csv' # изначальная таблица отделов
ADDRESS_DEPARTMENTS = 'app/data/Depertments_changed.json' # таблица отделов
ADDRESS_PERSONS = 'app/data/persons.json' # таблица соотрудников
ADDRESS_PERSONS_FULL = 'app/data/persons.xlsx' # изначальная таблица соотрудников


###-----------------------------------------------------------------------------
### Функции создания и настройки таблиц
###-----------------------------------------------------------------------------


### Создает файл с состояниями
### input: -
### output: -
def create_stack_file_json():
    table = pd.DataFrame({'user_id' : [None], 'stack' : [None]})
    table = table.dropna()
    table.to_json(ADDRESS_STACK)

### Создает столбы в таблице отделов
### input: filename - адрес файла таблицы отделов
### output: -
def create_depart_columns(filename):
    table = pd.DataFrame(columns=['name', 'number'])
    table.set_index(table['number'], inplace=True)
    table.sort_index(inplace=True)
    table.to_json(filename)

### Изменяет full_department для работы с базой
### input: -
### output: -
def change_departments():
    table = pd.read_csv(ADDRESS_DEPARTMENTS_FULL)
    table.set_index(table['id'], inplace=True)
    table.sort_index(inplace=True)
    del table['id']
    table['Отдел'] = table['Отдел'].str.lower()
    table['Ключи'] = table['Ключи'].str.lower()
    table.to_json(ADDRESS_DEPARTMENTS)

### Удаляет из xlsx не нужные столбцы, возвращает датафрейм
### input: filename - адрес файла таблицы соотрудников
### output: changed_table - измененная таблица соотрудников
def change_persons():
    table = pd.read_excel(ADDRESS_PERSONS_FULL)
    changed_table = table.loc[:,['Фамилия', 'Имя', 'Отчество', 'вн. номер', 'E-mail',             'мобильный \nномер']]
    changed_table.rename(columns={'мобильный \nномер' : 'мобильный номер'}, inplace=True)
    changed_table.set_index(changed_table['вн. номер'], inplace=True)
    del changed_table['вн. номер']
    changed_table.sort_index(inplace=True)
    changed_table.columns = changed_table.columns.str.strip() #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    changed_table['Фамилия'] = changed_table['Фамилия'].str.strip()
    changed_table['Имя'] = changed_table['Имя'].str.strip()
    changed_table['Отчество'] = changed_table['Отчество'].str.strip()
    changed_table = changed_table.dropna()

    changed_table.to_json(ADDRESS_PERSONS)


###-----------------------------------------------------------------------------
### Функции парсеров файлов и таблиц
###-----------------------------------------------------------------------------


### Парсер стека состояний: по id юзера достает стек состояний автомата из словаря
### input: autocall_class - экземпляр класса autocall, table - dataFrame из файла с состояниями
### output: res_stack - лист с состояниями автомата
def parse_session_from_table(autocall_class, table): # TODO: обеспечение абстрактности
    changed_table = table.loc[table['user_id'] == autocall_class._userID]

    # Отстуствует запись о user_id в файле
    if changed_table.size < 0 or changed_table.empty:
        return None

    res_stack = []
    parsing_stack = changed_table.iloc[0]['stack']
    if len(parsing_stack) == 0: # Если не найдено
        return None

    for str in parsing_stack:
        if str == 'stateA_start':
#             print("Распознано А/n") #debug
            res_stack.append(autocall_class.stateA_start)
        elif str == 'stateB_dep':
#             print("Распознано B/n") #debug
            res_stack.append(autocall_class.stateB_dep)
        elif str == 'stateC_per':
#             print("Распознано C/n") #debug
            res_stack.append(autocall_class.stateC_per)
        elif str == 'stateD_connect':
#             print("Распознано D/n") #debug
            res_stack.append(autocall_class.stateD_connect)
        elif str == 'stateE_connect_error':
#             print("Распознано E/n") #debug
            res_stack.append(autocall_class.stateE_connect_error)
        else:
            raise ErrorParser('Unexpected data in UsersStacks.json')
    return res_stack

### Ошибка парсера parser_session # TODO: создать файл ошибок и перенести в него
class ErrorParser(Exception):
    pass

### Парсер стека состояний: по id юзера достает стек состояний автомата из словаря
### input: autocall_class - экземпляр класса autocall
### output: res_stack - лист с состояниями автомата
def parse_session_from_file(autocall_class): #ToDo class -> instance
    try:
        table = pd.read_json(ADDRESS_STACK)
        return parse_session_from_table(autocall_class, table)
    except:
        return None

### Обновляет стек в таблице стеков
### input: autocall_class - экземпляр класса autocall, table - таблица стеков
### output: table - обновленная таблица стека
def update_stack_in_table(autocall_class, table):
    # Таблица не пустая
    if not table.empty:
        #Удаляем из таблицы старый стек
        table = table.loc[table['user_id'] == autocall_class._userID]
        if not table.empty: # Если не найдено записи о сессии
            table.iloc[0]['stack'] = autocall_class.getStack()
            return table

    table.loc[0] = [autocall_class._userID, autocall_class.getStack()]
    return table

### Обновляет стек в файле ADDRESS_STACK
### input: autocall_class - экземпляр класса autocall
### output: -
def update_stack_in_file(autocall_class):
#     try:
#         table_stack = pd.read_json(ADDRESS_STACK)
#     except:
#         create_stack_file_json()
    table_stack = pd.read_json(ADDRESS_STACK)
    table = update_stack_in_table(autocall_class, table_stack)
    table.to_json(ADDRESS_STACK)

### Удаляет сессию в таблице
### input: autocall_class - экземпляр класса autocall, table - таблица стеков
### output: table - обновленная таблица стека
def delete_session_in_table(autocall_class, table):
    table = table.loc[table['user_id'] == autocall_class._userID]
    table.iloc[0] = None
    return table

### Удаляет сессию в ADDRESS_STACK
### input: autocall_class - экземпляр класса autocall
### output: -
def delete_session_in_file(autocall_class):
    table = delete_session_in_table(autocall_class,  pd.read_json(ADDRESS_STACK))
    table.to_json(ADDRESS_STACK)


###-----------------------------------------------------------------------------
### Функции поиска в таблицах
###-----------------------------------------------------------------------------


### Ищет отдел по сообщению пользователя
### input: response - сообщение пользователя
### output: number - номер найденного отдела, fio - название отдела
def find_department(response):
    table_dep = pd.read_json(ADDRESS_DEPARTMENTS)
    table_pers = pd.read_json(ADDRESS_PERSONS)
    #segments = Normalize(response) # разбитие на токены в инфинитиве
    segments = response.lower().split(' ')

    # поиск по ключам
    list_keys_dep = table_dep['Ключи'].values
    for word in segments:
        for key_dep in list_keys_dep:
            if key_dep.find(';') != -1:
                splited_key = key_dep.split('; ')[:-1]
            else:
                splited_key = [key_dep]
            for key in splited_key:
                if word.startswith(key[:-2]):
                    cur_row_dep = table_dep.loc[table_dep['Ключи'] == key_dep]
                    number = cur_row_dep.iloc[0]['Руководитель']

                    currect_row_pers = table_pers.loc[number]
                    fio = currect_row_pers['Фамилия'] + ' ' + currect_row_pers['Имя'] + ' ' + currect_row_pers['Отчество']

                    return number, fio
    return None, None


### Ищет первое вхождение по номеру в таблице, возвращает номер и имя
### input: numbers - список найденных номеров в сообщении, table - таблица persons
### output: number - номер найденного соотрудника, fio - имя соотрудика
def find_num_person_from_table(numbers, table):
    for number in numbers:
        record = table.loc[number]
        if not record.empty:
            fio = record['Фамилия'] + ' ' + record['Имя'] + ' ' + record['Отчество']
            return number, fio
    return None, None

### Ищет первое вхождение по номеру в файле, возвращает номер и имя
### input: numbers - список найденных номеров в сообщении, table - таблица persons
### output: number - номер найденного соотрудника, fio - имя соотрудика
def find_num_person_from_file(numbers, filename):
    return find_num_person_from_table(numbers, pd.read_json(filename))

### Ищет name в таблице persons
### input: словарь name = {first : ..., middle : ..., last : ...} и таблицу persons
### output: номер и имя
def find_num_person_by_name_from_table(name, table):
    record = pd.DataFrame()
    record = find_fio_helper(name, table)
    if record.empty:
        #Если нет фамилии, проверяем имя-отчество
        record = table.loc[table['Имя'] == name.get('first')]
        record = record.loc[record['Отчество'] == name.get('middle')]
        if record.empty:
            #Только полное соответствие #Это лишнее!!!!!!! Недостижимый код
            record = table.loc[table['Имя'] == name.get('first')]
            record = record.loc[record['Отчество'] == name.get('middle')]
            record = record.loc[record['Фамилия'] == name.get('last')]
            if record.empty:
                #Соответсвий не найдено
                return None, None

    number = record.index[0]
    fio = record.iloc[0]['Фамилия'] + ' ' + record.iloc[0]['Имя'] + ' ' + record.iloc[0]['Отчество']
    return number, fio

### Все от Наташи проверяется на фамилию таблицы
### input: cловарь name = {first : ..., middle : ..., last : ...} и таблицу persons
### output: dataFrame pandas с записью о человеке или None
def find_fio_helper(name, table):
    record = pd.DataFrame()
    containers = ['last', 'middle', 'first']
    for container in containers:
        record = table.loc[table['Фамилия'] == name.get(container)]
        if not record.empty:
            return record
    return record


# In[24]:


# change_departments()
# change_persons()

#table_dep = pd.read_json(ADDRESS_DEPARTMENTS)
#table_pers = pd.read_json(ADDRESS_PERSONS)

# print(table_dep.loc[0])
# print(table_pers.loc[0])


# In[ ]:




