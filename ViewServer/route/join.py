from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse
import urllib
import json


class Join(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('join.html'), 200, headers)

    def post(self):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password == password2 and password != '' and password2 != '':
            data = {'name': name, 'email': email, 'password': password}
            jsonData = bytes(json.dumps(data).encode())
            req = urllib.request.Request("http://localhost:5001/user", data=jsonData)
            req.get_method = lambda: 'post'
            jsonResult = urllib.request.urlopen(req).read()
            result = json.loads(jsonResult.decode('utf-8'))['success']
            if result == 'ok':
                return redirect('/login')
            else:
                return redirect('/join')
        else:
            return redirect('/join')
