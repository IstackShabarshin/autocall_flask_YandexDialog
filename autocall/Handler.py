#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from autocall import autocall
from speech_kit import speech_kit

def handler(event, context, is_audio=false):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    text = ''
    end_session = False
    is_new = False #event['session']['new']
    autocall_handeler = autocall(event['session']['user_id'])

    if is_audio:
        req_text = speech_kit.recognize(context)
        resp_text = autocall_handler.update(req_text)
        resp = speech_kit.synthesize(resq_text).content
        resutl_data = {
            'Content-Type': 'audio/ogg'
            'Content' : resp
        }

    elif 'request' in event and 'original_utterance' in event['request'] and len(event['request']['original_utterance']) > 0:
        resp = autocall_handler.update(event['request']['original_utterance']) # передача сообщения автомату

        result_data = {
            'version': event['version'],
            'session': event['session'],
            'response': {
                # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                'text': resp,
                # Don't finish the session after this response.
                'end_session': end_session
            }
        }

    return json.dumps(result_data,  ensure_ascii=False)


# In[ ]:




