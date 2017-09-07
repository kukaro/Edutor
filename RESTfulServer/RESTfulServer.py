from flask import Flask, render_template, make_response, redirect, request
from flask_restful import Resource, Api, reqparse

# Make Instance
app = Flask(__name__)
api = Api(app)

'''
class Root(Resource):
    def get(self):
        try:
            return 'get'
        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            data = {'delete': 'delete', 'h': 'hello'}
            return data, 201
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Root, '/')
'''


class Root(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


api.add_resource(Root, '/')

if __name__ == '__main__':
    app.run(port=5001)
