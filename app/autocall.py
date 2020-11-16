#!/usr/bin/env python
# coding: utf-8

# In[1]:


###-----------------------------------------------------------------------------
### Инициализация библиотек
###-----------------------------------------------------------------------------

from pandas import(
    read_json # для загрузки таблиц из json
)
import app.data_parsers as parser # для работы с таблицами таблиц 
from app.StackFSM import StackFSM # для реализации автомата 
#from app.NatashaParser import (
#    FindNames, # поиск имен в сообщений
#    SplitOnSegments, # для разбиения на токены сообщений
#    Normalize,  # для приведения к инфинитиву
#    SplitOnLemmas
#)
from app.NatashaParser.natasha_server import conn_natasha
import json

###-----------------------------------------------------------------------------
### Реализация автомата
###-----------------------------------------------------------------------------


# Класс автомата автоответчика
class autocall(StackFSM):
    
    # Конструктор
    def __init__(self, state):
        super().__init__()
        users_stacks = self.parse_session(state)
        
        # Если в state была сессия
        if users_stacks != None:
            self._stack = users_stacks

        # state не содержит информацию о сессии    
        else: 
            # Заносим в стек стартовое состояние
            self.pushState(self.state0_init)
                
    # Обновляет запись сессии 
    def updateFile(self):
        pass
        #parser.update_stack_in_file(self)
    
    # Удаляет запись о сессии 
    def removeStack(self):
        pass
#         super().removeStack()
#         parser.delete_session_in_file(self)
    
    def parse_session(self, state):
        res_stack = []
        if state == 'stateA_start':
#             print("Распознано А/n") #debug
            res_stack.append(self.stateA_start)
        elif state == 'stateB_dep':
#             print("Распознано B/n") #debug
            res_stack.append(self.stateB_dep)
        elif state == 'stateC_per':
#             print("Распознано C/n") #debug
            res_stack.append(self.stateC_per)
        elif state == 'stateD_connect':
#             print("Распознано D/n") #debug
            res_stack.append(self.stateD_connect)
        elif state == 'stateE_connect_error':
#             print("Распознано E/n") #debug
            res_stack.append(self.stateE_connect_error)
        else:
            return None
            #raise ErrorParser('Unexpected data in UsersStacks.json')
        return res_stack
        
   
    # Заглушка для передачи звонка Cisco
    def connect_to_Cisco(self, number): # TODO: передача cisco
#        return True
         return False
    
    ###-----------------------------------------------------------------------------
    ### Реализация состояний
    ###-----------------------------------------------------------------------------
    
    def state0_init(self, request):
        self.popState()
        self.pushState(self.stateA_start)
        self.updateFile()
        return 'Добрый день! Вас соединить с соотрудником или отделом?'
    
    def stateA_start(self, request):
        tokens = request.split(' ')
        for word in tokens: # TODO: * -> inf
            #word = token.text
            if word.startswith('отдел'):
                self.popState()
                self.pushState(self.stateB_dep)
                self.updateFile()
                return 'Назовите название или номер отдела'
            elif word.startswith('соотрудник'):
                self.popState()
                self.pushState(self.stateC_per)
                self.updateFile()
                return 'Назовите имя или номер соотрудника'
        return 'Вас соединить с соотрудником или отделом?'
                
    def stateB_dep(self, request):
        number, fio  = parser.find_department(request)
        
        if number != None:
            return self.stateD_connect(number, fio)
        else:
            return "Извините, не удалось найти такого отдела"
        
    def stateC_per(self, request):
        table = read_json(parser.ADDRESS_PERSONS)

        #Сначала ищем номера сотрудников, если они есть
        potention_numbers = conn_natasha(request, '-s') #Connect to natasha_server for execute SplitOnSegments
        potention_numbers = [int(_) for _ in potention_numbers if _.isdigit()]
        number, fio = parser.find_num_person_from_table(potention_numbers, table)
        if number != None:
            return self.stateD_connect(number, fio)

        #Теперь ищем FIO
        name_list = conn_natasha(request, '-fn') # парсим на имена через natasha_server
        print(name_list, flush=True)
        if len(name_list) == 0:
            return "Извините, не удалось найти такого соотрудника"
        if len(name_list) >= 1:
            name_dict = {'last': name_list[0]}
        if len(name_list) >= 2:
            name_dict.update({'middle': name_list[1]})
        if len(name_list) >= 3:
            name_dict.update({'first': name_list[2]})
        #name_dict = {'last': name_list[0], 'middle': name_list[1], 'first': name_list[2]}
#         print('Имена, которые нашла Наташа: \n' + str(names)) #debug
#         print('\n' + str(len(names)) + '\n') #debug
        
        #for name in names.items():
        number, fio = parser.find_num_person_by_name_from_table(name_dict, table) #To do: только фамилии
        if fio != None:
            return self.stateD_connect(number, fio)
        return "Извините, не удалось найти такого соотрудника"
    
    def stateD_connect(self, number, fio):
        self.popState()
        if self.connect_to_Cisco(number): # передача разговора Cisco
            self.removeStack()
            return 'Переключаю на пользователя ' + fio 
        else:
            self.pushState(self.stateE_connect_error)
            self.updateFile()
            return 'Извините, не удалось дозвониться до ' + fio + ', могу ли я еще чем-нибудь помочь?' #!!!!
    
    
    def stateE_connect_error(self, request):
        tokens = request.split(' ')
        for word in tokens:
            if word.startswith('да'):
                self.popState()
                self.pushState(self.stateA_start)
                self.updateFile()
                return 'Вас соединить с соотрудником или отделом?'

        self.popState()
        self.removeStack()
        return "До свидания"


# In[ ]:




