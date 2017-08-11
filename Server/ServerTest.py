from flask import Flask, render_template, make_response
from flask_restful import Resource, Api, reqparse

# Make Instance
app = Flask(__name__)
api = Api(app)


# Define Route

class ReadIndex(Resource):
    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'), 200, headers)
        except Exception as e:
            return {'error': str(e)}


api.add_resource(ReadIndex, '/')

if __name__ == '__main__':
    app.run()
