from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse
import requests

# Make Instance
app = Flask(__name__)
api = Api(app)


# Define Route
class Answer(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('answer-frame.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}


class Question(Resource):
    def get(self, year, month, subject):
        try:
            print('Question:' + year)
            headers = {'Content-Type': 'text/html'}
            return render_template('question-frame.html', year=year, month=month, subject=subject)
        except Exception as e:
            return {'error': str(e)}

    def post(self, year, month, subject):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('question-frame.html', year=year, month=month, subject=subject), 200,
                                 headers)
        except Exception as e:
            return {'error': str(e)}


class QuestionList(Resource):
    def get(self):
        try:
            return redirect('/question/2011/3/수학')
        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            year = request.form.get('year')
            print('QuestionList:%s' % year)
            return redirect('/question/' + year + '/3/수학')
        except Exception as e:
            return {'error': str(e)}


class Index(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}


class Chatbot(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('chatbot-frame.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}


class Chatbot_input(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('chatbot-input-frame.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}


class RootPage(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}


api.add_resource(RootPage, '/')
api.add_resource(Index, '/index')
api.add_resource(QuestionList, '/question', endpoint='/question')
api.add_resource(Question, '/question/<year>/<month>/<subject>')
api.add_resource(Answer, '/answer')
api.add_resource(Chatbot, '/chatbot')
api.add_resource(Chatbot_input, '/chatbot-input')

if __name__ == '__main__':
    app.run()
