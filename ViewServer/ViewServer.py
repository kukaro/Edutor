import datetime

from flask import Flask, session
from flask_restful import Api
from flask_socketio import SocketIO, emit

from module.chatbot import chatbot
from module.utils.dialog import byteArrayToStr, addDialog
from route.chatbot_body import ChatbotBody
from route.chatbot_input import ChatbotInput
from route.chatbot_user import ChatbotUser
from route.join import Join
from route.left import Left
from route.login import Login
from route.right import Right
from route.root import Root
from route.term_answer import TermAnswer
from route.term_question import TermQuestion
from route.testEraseSession import TestEraseSession
from route.hello import Hello

# Make Instance
app = Flask(__name__)
api = Api(app)
app.secret_key = "secret"
socketio = SocketIO(app)


@socketio.on('connect', namespace='/mynamespace')
def connect():
    # emit('response', {'data': 'Connected'})
    pass


@socketio.on('test', namespace='/mynamespace')
def test(msg):
    print(msg)


@socketio.on('dialog', namespace='/mynamespace')
def dialog(msg):
    dialog = byteArrayToStr(msg['data'])
    name = byteArrayToStr(msg['name'])
    email = byteArrayToStr(msg['email'])
    callState = byteArrayToStr(msg['callState'])
    time = str(datetime.datetime.now())
    print('socket on dialog : ')
    print(dialog, name, email, time, callState)
    if 'isLogin' in session:
        if addDialog(dialog, name, email, time, callState):
            emit('dialogConfirm', {'confirm': True, 'dialog': dialog, 'time': time, 'callState': callState})
        else:
            emit('dialogConfirm', {'confirm': False})
    else:
        emit('dialogConfirm', {'confirm': False})


@socketio.on('callChatbot', namespace='/mynamespace')
def callChat(msg):
    try:
        if 'state' in msg:
            if msg['state']:
                tmp = chatbot(msg)
                if 'dialog' in tmp:
                    emit('ansChatbot', tmp)
                else:
                    emit('storeTermDataChatbot', tmp)
    except Exception as e:
        print('exception:' + e)
        emit('ansChatbot', {'dialog': '실패하였습니다.', 'callState': 'None'})


@socketio.on('callTermTest', namespace='/mynamespace')
def callTermTest(msg):
    if 'state' in msg:
        if msg['state']:
            # tmp = chatbot(msg['filename'])
            filename = byteArrayToStr(msg['filename'])
            print('socket on callTermTest : ')
            print(filename)
            emit('ansChatbot', {'dialog': '문제를 푸시겠습니까?', 'callState': 'termTest', 'filename': filename})


@socketio.on('markingTermChatbot', namespace='/mynamespace')
def markingTermChatbot(msg):
    filename = byteArrayToStr(msg['filename'])
    termCount = byteArrayToStr(msg['termCount'])
    termArr = []
    i = 0
    size = 0
    addStr = ''
    for termE in msg['termArr']:
        if termE is None:
            termArr.append(None)
        else:
            termArr.append(byteArrayToStr(termE))
            size += 1
            addStr += str(i + 1) + '번 '
        i += 1
    print('size:' + str(size))
    print('termCount:' + str(termCount))
    if str(termCount) != str(size):
        emit('ansChatbot',
             {'dialog': '아직 문제를 다 풀지 못했습니다.<br> 푼 문제는 ' + addStr + '입니다.', 'callState': 'testTermOK',
              'filename': filename})
    elif size == 0:
        emit('ansChatbot',
             {'dialog': '아직 문제를 다 풀지 못했습니다.<br> 푼 문제는 없습니다.', 'callState': 'testTermOK',
              'filename': filename})
    else:
        emit('ansChatbot',
             {'dialog': '문제를 모두 푸셨습니다. 채점을 시작합니다.', 'callState': 'testTermMarking',
              'filename': filename})
        msg['callState'] = b'testTermMarking'
        tmp = chatbot(msg)


'''
class Root(Resource):
    def get(self):
        try:
            req = urllib.request.Request("http://localhost:5001/")
            req.get_method = lambda: 'DELETE'
            data = urllib.request.urlopen(req).read()
            jsonData = json.loads(data.decode('utf-8'))
            return jsonData
        except Exception as e:
            return {'error in  /': str(e)}


api.add_resource(Root, '/')
'''

# Route
api.add_resource(Root, '/')
api.add_resource(Join, '/join')
api.add_resource(Login, '/login')
api.add_resource(ChatbotBody, '/chatbot-body')
api.add_resource(ChatbotInput, '/chatbot-input')
api.add_resource(TermAnswer, '/term-answer')
api.add_resource(TermQuestion, '/term-question')
api.add_resource(Left, '/left')
api.add_resource(Right, '/right')
api.add_resource(ChatbotUser, '/chatbot-user')
api.add_resource(Hello, '/hello')

# Test Route
api.add_resource(TestEraseSession, '/erase-session')

if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=True, port=5000)
