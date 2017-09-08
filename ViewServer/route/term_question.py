from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse


class TermQuestion(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('term-question-frame.html'), 200,
                             headers)

    def post(self):
        try:
            headers = {'Content-Type': 'text/html'}
            # year = request.form.get('year')
            # month = request.form.get('month')
            # subject = request.form.get('subject')
            return make_response(render_template('term-question-frame.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}
