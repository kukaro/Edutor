from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from pymongo import MongoClient
from module.utils.csv_reader import readCSV
import json

mongo = MongoClient()
db = mongo.edutor
wrong_answer = db.wrong_answer


class WrongAnswer(Resource):
    def get(self):
        jsonData = request.get_data()
        data = json.loads(jsonData.decode())
        print(data)
        if data['subject'] == '수학':
            data['subject'] += '가형'
        result = wrong_answer.find_one({'term': {
            'year': data['year'][:4],
            'subject': data['subject'],
            'term_type': data['term_type']
        }})
        print(result)
        return result['wrong_answer']

    def post(self):
        jsonData = request.get_data()
        data = json.loads(jsonData.decode())
        filenameW = data['wrong_answer_dir']
        fileW = readCSV(filenameW)
        file_header = fileW[0]
        sw = True
        print(fileW[0])
        if wrong_answer.find_one({'term': {
            'year': data['year'][:4],
            'subject': data['subject'],
            'term_type': data['term_type']
        }}) is None:
            if data['term_type'] == '수능':
                query = [{'term': {
                    'year': data['year'][:4],
                    'subject': data['subject'],
                    'term_type': data['term_type'],

                }, 'wrong_answer': {}}]
                for row in fileW:
                    tmp = {}
                    if sw:
                        sw = False
                    else:
                        for i in range(len(row)):
                            tmp[file_header[i]] = row[i]
                        query[0]['wrong_answer'][str(row[0])] = tmp
                print(query)
                wrong_answer.insert(query)
        return {'success': 'ok'}
