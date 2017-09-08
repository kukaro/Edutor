from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse


class Root(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        if 'isLogin' in session:
            name = session['name']
            email = session['email']
            print('result : ')
            print(name + ":" + email)
            return make_response(render_template('index.html', name=name, email=email), 200, headers)
        else:
            return redirect('/login')
