from flask import Flask, render_template, make_response, redirect, request, session
from flask_restful import Resource, Api, reqparse
import json
import urllib


class MypageInfo(Resource):
    def get(self):
        email = session['email']
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('mypage-info.html'), 200, headers)
    def post(self):
        email = session['email']
        headers = {'Content-Type': 'text/html'}
        print(request.form.get('data'))
        return make_response(render_template('mypage-info.html'), 200, headers)
