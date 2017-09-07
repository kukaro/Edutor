from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse

class Right(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('view-right-frame.html'), 200, headers)