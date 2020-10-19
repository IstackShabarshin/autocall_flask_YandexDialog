from app import app
from app import main, dbParser
from flask import (
    request,
    session
)

selectId = dbParser.selectId
insertSession = dbParser.insertSession
changeState = dbParser.changeState
deleteSession = dbParser.deleteSession

@app.route('/', methods=["GET", "POST"])
def call():
    if request.method == "GET":
        if 'state' in session and len(session['state']) > 0:
            text = request.args.get('text')
            if text == None or len(text) == 0:
                text = 'default'
            session['state'], resp = main.handler(session['state'][0], text)
        else:
            session['state'], resp = main.handler(None, 'hi')
        session.modified = True
        return str(resp) + '\n'

    if request.method == "POST":
       data = request.get_json(force=True)
       return data
       #if 'user_id' in data:
          # return {"ok": True}
       #else:
          # return {"ok": False}

@app.route('/del')
def del_session():
    session['state'] =  ''
    session.modified = True
    return {"ok": True}

@app.route('/yandexDialog', methods=["POST"])
def yandexDialog():
    data = request.get_json(force=True)
    requestText = data["request"]["original_utterance"]
    sessionId = data["session"]["session_id"]
    if data["session"]["new"] == True:
        state, text = main.handler(None, requestText)
        insertSession(sessionId, state[0])
    else:
        state = selectId(sessionId)
       # print(requestText)
        state, text = main.handler(state, requestText)
       # print(state)
        changeState(sessionId, state[0])


    return  {"response": {"text": text, "end_session": False}, "version": "1.0"}
