import os
import unicodedata
from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse
from flask_socketio import SocketIO, emit
from route.join import Join
from route.root import Root
from route.chatbot_body import ChatbotBody
from route.chatbot_input import ChatbotInput
from route.term_answer import TermAnswer
from route.term_question import TermQuestion
from route.left import Left
from route.right import Right
import urllib.request
import json

# Make Instance
app = Flask(__name__)
api = Api(app)
app.secret_key = "secret"
socketio = SocketIO(app)


@socketio.on('connect', namespace='/mynamespace')
def connect():
    # emit("response", {'data': 'Connected'})
    pass


@socketio.on('test', namespace='/mynamespace')
def test(msg):
    print(msg)


@socketio.on('dialog', namespace='/mynamespace')
def dialog(msg):
    print(msg['data'])
    print(chr(msg['data'][0]))


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

api.add_resource(Root, '/')
api.add_resource(Join, '/join')
api.add_resource(ChatbotBody, '/chatbot-body')
api.add_resource(ChatbotInput, '/chatbot-input')
api.add_resource(TermAnswer, '/term-answer')
api.add_resource(TermQuestion, '/term-question')
api.add_resource(Left, '/left')
api.add_resource(Right, '/right')

if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=True, port=5000)
