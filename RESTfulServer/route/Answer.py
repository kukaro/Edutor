from flask import Flask, render_template, make_response, redirect, request
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
        print(dataList[len(dataList) - 1])
