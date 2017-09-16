from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse


class TestEraseSession(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        print('After Erase :')
        print(session.keys())
        if 'isLogin' in session:
            session.pop('isLogin')
            session.pop('name')
            session.pop('email')
            print('Before Erase : ')
            print(session.keys())
            return redirect('/login')
        else:
            return redirect('/login')
