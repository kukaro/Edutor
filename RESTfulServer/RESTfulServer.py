from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from pymongo import MongoClient
import json

from route.Answer import Answer

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'edutor'

mysql.init_app(app)
api = Api(app)

mongo = MongoClient()
db = mongo.edutor
dialog = db.dialog
question = db.question


class User(Resource):
    def post(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "INSERT INTO USER(name, email, password) VALUES('%s', '%s', '%s');" % (
                data['name'], data['email'], data['password'])

            cursor.execute(query)
            conn.commit()
            conn.close()

            return {'success': 'ok'}

        except Exception as e:
            return {'success': 'no'}

    def get(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "SELECT * FROM USER WHERE email = '%s'" % data['email']

            cursor.execute(query)
            row = cursor.fetchall()
            rowToDict = {'data':{'name': row[0][0], 'email': row[0][1], 'password': row[0][2]}}
            print('result : ')
            print(rowToDict)
            return rowToDict

        except Exception as e:
            data = {'data': 'no'}
            print('result : ')
            print(data)
            return data

    def put(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "UPDATE USER SET name='%s', password='%s' WHERE email='%s'" % (
                data['name'], data['password'], data['email'])

            cursor.execute(query)
            conn.commit()
            conn.close()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "DELETE FROM USER WHERE email='%s'" % data['email']

            cursor.execute(query)
            cursor.fetchall()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}


class Bot(Resource):
    def post(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "INSERT INTO BOT(name, owner) VALUES('%s', '%s');" % (data['name'], data['owner'])

            cursor.execute(query)
            conn.commit()
            conn.close()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "SELECT * FROM BOT WHERE owner='%s'" % data['owner']

            cursor.execute(query)
            row = cursor.fetchall()

            return json.dumps(row)

        except Exception as e:
            return {'error': str(e)}

    def put(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "UPDATE BOT SET name='%s' WHERE owner='%s'" % data['owner']

            cursor.execute(query)
            conn.commit()
            conn.close()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "DELETE FROM BOT WHERE owner='%s'" % data['owner']

            cursor.execute(query)
            cursor.fetchall()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}


class Term(Resource):
    def post(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "INSERT INTO TERM(year, month, subject, term_type) VALUES('%s', '%s', '%s', '%s');" % (
                data['year'], data['month'], data['subject'], data['term_type'])

            cursor.execute(query)
            conn.commit()
            conn.close()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "SELECT * FROM TERM WHERE year='%s' and month='%s' and subject='%s' and term_type='%s'" % (
                data['year'], data['month'], data['subject'], data['term_type'])

            cursor.execute(query)
            row = cursor.fetchall()

            return json.dumps(row)

        except Exception as e:
            return {'error': str(e)}

    def put(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "UPDATE TERM SET year='%s', month='%s', subject='%s', term_type='%s' WHERE year='%s' and month='%s' and subject='%s' and term_type='%s'" % (
                data['year'], data['month'], data['subject'], data['term_type'])

            cursor.execute(query)
            conn.commit()
            conn.close()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "DELETE FROM TERM WHERE year='%s' and month='%s' and subject='%s' and term_type='%s'" % (
                data['year'], data['month'], data['subject'], data['term_type'])

            cursor.execute(query)
            cursor.fetchall()

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}


class Dialog(Resource):
    def post(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))
            print('result : ')
            print(data)
            dialog.insert([
                {
                    'name': data['name'],
                    'time': data['time'],
                    'message': data['message'],
                }
            ])

            return {'success': 'ok'}

        except Exception as e:
            return {'success': 'no'}

    def get(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            row = dialog.find_one({'time': data['time']})

            return json.dumps(row)

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            dialog.remove(
                {
                    'time': data['time']
                }
            )

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}


class Question(Resource):
    def post(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            question.insert([
                {
                    'term': {
                        'year': data['term']['year'],
                        'month': data['term']['month'],
                        'subject': data['term']['subject'],
                        'term_type': data['term']['term_type']
                    },
                    'number': data['number'],
                    'title': data['title'],
                    'content': data['content'],
                    'answer_type': data['title'],
                    'answer': {
                        'subjective': data['answer']['subjective'],
                        'objective': {
                            'answer_number': data['answer']['objective']['answer_number'],
                            'answer_content': data['answer']['objective']['answer_content']
                        }
                    },
                    'right_answer': data['right_answer'],
                    'question_type': data['question_type']
                }
            ])

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            row = db.dialog.find_one({'time': data['time']})

            return row

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            jsonData = request.get_data()
            data = json.loads(jsonData.decode('utf-8'))

            db.dialog.remove(
                {
                    'time': data['time']
                }
            )

            return {'success': 'ok'}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(User, '/user')
api.add_resource(Bot, '/bot')
api.add_resource(Term, '/term', endpoint='/question')
api.add_resource(Dialog, '/dialog')
api.add_resource(Question, '/question')
api.add_resource(Answer, '/answer')

if __name__ == '__main__':
    app.run(port=5001)

    #
    # db.users.insert_many([
    #     {
    #         'id': 'wlsgk0323',
    #         'password': 'edutor',
    #         'name': '임진하',
    #         'email': 'ss@ddd',
    #     },
    #
    # ])
    # print(db.users.find_one({'id': 'wlsgk0323'}))
