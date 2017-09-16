from flask import Flask, render_template, make_response, redirect, request, send_from_directory
from flask_restful import Resource, Api, reqparse


class TermQuestion(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            #filename = request.form.get('filename')
            filename = request.args['filename']
            print('Get TermQuestion : ')
            print(filename[22:])
            directory = '/Users/jiharu/Desktop/'
            #binary_pdf = '/Users/jiharu/Desktop/2014년도 6월 영어 모의고사.pdf'
            #response = make_response(binary_pdf)
            #response.headers['Content-Type'] = 'application/pdf'
            #response.headers['Content-Disposition'] = 'inline; filename=%s' % '2016년도 10월 국어 모의고사.pdf'
            return send_from_directory(directory, filename[22:])
            #return make_response(render_template('term-question-frame.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            headers = {'Content-Type': 'text/html'}
            filename = request.form.get('filename')
            print('Post TermQuestion : ')
            print(filename)
            # year = request.form.get('year')
            # month = request.form.get('month')
            # subject = request.form.get('subject')
            # return make_response(xml, 200, headers)
            #return make_response(render_template('term-question-frame.html'), 200, headers)
            return send_from_directory(filename)
        except Exception as e:
            return {'error': str(e)}
