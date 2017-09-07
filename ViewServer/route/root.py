from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse

class Root(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)