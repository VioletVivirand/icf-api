# Start with: python api.py
from flask import Flask, redirect, abort, send_from_directory
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse, abort
# from createjson_disabilities import createjson
from createjson_prevalence import createjson

app = Flask(__name__)
cors = CORS(app, resources={
    r"/api/*": {"origins": "*"}
    })
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('sex')
parser.add_argument('smallerAge')
parser.add_argument('biggerAge')
parser.add_argument('level')
parser.add_argument('codet')
parser.add_argument('desc')

@app.route('/')
def index():
    return 'It Works!'

@app.route('/assets/json/<path:path>')
def send_json(path):
    return send_from_directory('assets/json', path)

class getData(Resource):
    def get(self):
        args = dict(parser.parse_args())
        # TODO: 把 404 的回傳拉來這邊
        return createjson(args)
    
api.add_resource(getData, '/api')

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0')
