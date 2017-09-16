from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse
import json
import urllib


class MypageIndex(Resource):
    def get(self):
        email = session['email']
        headers = {'Content-Type': 'text/html'}
        data = {'email': session['email']}
        jsonData = bytes(json.dumps(data).encode())
        print('Mypage Index get Result : ')
        print(jsonData)
        req = urllib.request.Request("http://localhost:5001/answer", data=jsonData)
        req.get_method = lambda: 'get'
        jsonResult = urllib.request.urlopen(req).read()
        result = json.loads(jsonResult.decode())
        oracle = {}
        tmp = {}
        for ele in result['data']:
            if ele['term']['subject'] in oracle:
                tmp[ele['term']['subject']] += 1
                oracle[ele['term']['subject']] += ele['grade']
            else:
                tmp[ele['term']['subject']] = 1
                oracle[ele['term']['subject']] = ele['grade']
        for k in tmp.keys():
            oracle[k] /= tmp[k]
        return make_response(render_template('mypage-index.html', data=result['data'],oracle=oracle), 200, headers)
