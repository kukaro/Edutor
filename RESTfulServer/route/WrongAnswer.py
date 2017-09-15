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
        pass

    def post(self):
        jsonData = request.get_data()
        data = json.loads(jsonData.decode())
        filenameW = data['wrong_answer_dir']
        fileW = readCSV(filenameW)
        file_header = fileW[0]
        sw = True
        print(fileW[0])
        if data['term_type'] == '수능':
            query = [{'term': {
                'year': data['year'][:4],
                'subject': data['subject'],
                'term_type': data['term_type'],
                'wrong_answer': {}
            }}]
            for row in fileW:
                tmp = {}
                if sw:
                    sw = False
                else:
                    for i in len(row):
                        tmp[fileW[i]] = row[i]
                query['wrong_answer'][str(row[0])] = tmp
            print(query)
