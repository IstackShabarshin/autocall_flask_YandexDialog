#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from app.autocall import autocall 

def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    text = ''
    end_session = False
    is_new = False #event['session']['new']
    
    if 'request' in event and 'original_utterance' in event['request'] and len(event['request']['original_utterance']) > 0:
        autocall_handler = autocall(event['session']['user_id']) # инициализация класса автомата
        text = autocall_handler.update(event['request']['original_utterance']) # передача сообщения автомату
#         if cur_text != '':
#             text = cur_text
        
    
    result_data = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
            'text': text,
            # Don't finish the session after this response.
            'end_session': end_session
        }
    }
    return json.dumps(result_data,  ensure_ascii=False)


# In[ ]:




