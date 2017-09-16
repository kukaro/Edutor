from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse
import urllib
import json


class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        data = {'email': email, 'password': password}
        jsonData = bytes(json.dumps(data).encode())
        req = urllib.request.Request("http://localhost:5001/user", data=jsonData)
        req.get_method = lambda: 'get'
        jsonResult = urllib.request.urlopen(req).read()
        result = json.loads(jsonResult.decode())
        print('result : ')
        print(result)
        if result['data'] != 'no' and result['data']['password'] == data['password']:
            session['isLogin'] = True
            session['email'] = result['data']['email']
            session['name'] = result['data']['name']
            return redirect('/')
        else:
            return redirect('/login')
