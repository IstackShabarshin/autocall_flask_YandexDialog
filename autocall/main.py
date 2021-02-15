#!/usr/bin/env python
# coding: utf-8

# In[1]:

import autocall.autocaller as fsm
from speech_kit import speech_kit

def handler(state, req, is_audio=False):
    if is_audio == True:
        text = speech_kit.recognize(req)
        print(text)
        text = text['result']
    else:
        text = req

    ac = fsm.autocall(state)
    resp = ac.update(text)
    session = ac.getStack()
    print(session)

    if is_audio == True:
        resp = speech_kit.synthesize(resp)
        print(resp)
        resp = resp.content

    if session != None:
        return session, resp
    else:
        return None, resp
