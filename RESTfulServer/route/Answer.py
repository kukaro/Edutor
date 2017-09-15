from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from pymongo import MongoClient
import json

mongo = MongoClient()
db = mongo.edutor
answer = db.answer


class Answer(Resource):
    def get(self):
        pass

    def post(self):
        jsonData = request.get_data()
        data = json.loads(jsonData.decode('utf-8'))
        dataList = data['filename'].split('/')
        print('Answer Post')
        print(data)
        print(dataList)
        termList = dataList[len(dataList) - 1].split(' ')
        print(termList)
        try:
            if 'email' in data:
                if 'email' is not None:
                    if termList[len(termList) - 1].find('수능') >= 0:
                        answer.insert([
                            {
                                'email': data['email'],
                                'term': {
                                    'year': termList[0][:4],
                                    'subject': termList[1],
                                    'term_type': '수능'
                                },
                                'answer_elements': data['termArr']
                            }
                        ])
                        return {'success': 'ok', 'term_type': '수능'}
                    elif termList[len(termList) - 1].find('모의고사') >= 0:
                        answer.insert([
                            {
                                'email': data['email'],
                                'term': {
                                    'year': termList[0][:4],
                                    'month': termList[1],
                                    'subject': termList[2],
                                    'term_type': '모의고사'
                                },
                                'answer_elements': data['termArr']
                            }
                        ])
                        return {'success': 'ok', 'term_type': '모의고사'}
                    else:
                        return {'success': 'no', 'comment': 'illegal term_type'}
                else:
                    return {'success': 'no', 'comment': 'email is none'}
            else:
                return {'success': 'no', 'comment': 'data has not email'}
        except Exception as e:
            print('Answer Post Error is ' + e)
            return {'success': 'no', 'comment': 'exception'}
