import datetime

from flask import Flask, session
from flask_restful import Api
from flask_socketio import SocketIO, emit

from module.chatbot import chatbot
from module.utils.dialog import byteArrayToStr, addDialog
from module.utils.term_slate import get_slate
from module.utils.term_crolling import get_term

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
    time = str(datetime.datetime.now())
    print('socket on dialog : ')
    print(dialog, name, email, time)
    if 'isLogin' in session:
        if addDialog(dialog, name, email, time):
            emit('dialogConfirm', {'confirm': True, 'dialog': dialog, 'time': time})
        else:
            emit('dialogConfirm', {'confirm': False})
    else:
        emit('dialogConfirm', {'confirm': False})


@socketio.on('callChatbot', namespace='/mynamespace')
def callChat(msg):
    if msg['state'] == True:
        tmp = chatbot(msg['dialog'])
        emit('ansChatbot', {'dialog': tmp})


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

# Test Route
api.add_resource(TestEraseSession, '/erase-session')

if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=True, port=5000)