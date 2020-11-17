#!/usr/bin/env python
# coding: utf-8

# In[1]:

import autocall.autocaller as fsm

def handler(state, text):
    ac = fsm.autocall(state)
    resp = ac.update(text)
    session = ac.getStack()
    if session != None:
        return session, resp
    else:
        return None, resp
