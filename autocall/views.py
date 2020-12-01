from autocall import app
from autocall import main, dbParser
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
    if request.method == "POST":
        if 'state' in session and len(session['state']) > 0:
            req_audio = request.get_data()
            if req_audio == None or len(req_audio) == 0:
                return {'error': 'not found audio'}
            session['state'], resp = main.handler(session['state'][0], req_audio, is_audio=True)
        else:
            return {'error': 'not found session: maybe y need init GET?'}
        session.modified = True
        return resp

    if request.method == "GET":
        if not 'state' in session:
            session['state'], resp = main.handler(None, 'hi')
            session.modified = True
            return str(resp)
        else:
            return {'error': 'not init request: maybe y need POST?'}

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
