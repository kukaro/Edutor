from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from pymongo import MongoClient
from module.utils.csv_reader import readCSV
import json

mongo = MongoClient()
db = mongo.edutor
point_cut = db.point_cut


class PointCut(Resource):
    def get(self):
        pass

    def post(self):
        jsonData = request.get_data()
        data = json.loads(jsonData.decode())
        filenameP = data['point_cut_dir']
        fileP = readCSV(filenameP)
        file_header = fileP[0]
        sw = True
        print(fileP[0])
        if data['term_type'] == '수능':
            query = [{'term': {
                'year': data['year'][:4],
                'subject': data['subject'],
                'term_type': data['term_type'],
                'point_cut': {}
            }}]
            for row in fileP:
                tmp = {}
                if sw:
                    sw = False
                else:
                    for i in len(row):
                        tmp[fileP[i]] = row[i]
                query['point_cut'][str(row[0])] = tmp
            print(query)
            #point_cut.insert()
