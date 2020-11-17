#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import deque

# Класс реализующий логику FSM
class StackFSM: #TODO RENAME!
    def __init__(self):#deque()):
        self._stack = []
 
    def update(self, text):
        currentStateFunction = self.getCurrentState()

        if (currentStateFunction != None):
            if text != None and text != '':
                return currentStateFunction(text)
            else:
                return currentStateFunction('default')
        else:
            raise StackError("Стек пуст")
    
    def removeStack(self):
        self._stack = []
 
    def popState(self):
        return self._stack.pop()
 
    def pushState(self, state):
        if (self.getCurrentState() != state):
            self._stack.append(state)
 
    def getCurrentState(self):
        length = len(self._stack)
        if (length > 0):
            return self._stack[length - 1]
        else:
            return None
        
    def getStack(self):
        res_stack = []
        for elem in self._stack:
            res_stack.append(elem.__name__)
        res_stack.reverse()
        return res_stack

class StackError(Exception):
    pass


# In[ ]:




