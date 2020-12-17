import json
import os

from flask import Flask, request
from flask_restful import Api, Resource

from Joker import Joker

app = Flask(__name__)
api = Api(app)

joker = Joker(modelname="JOKE_5", mappingname="JOKE_5")

@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container running on Heroku!'

# @api.resource('/complete_joke')
class JokeCompleter(Resource):
    def get(self):
        global joker
        text = request.args.get('text')
        return joker.getFullJoke(text)

# @api.resource('/get_next_word')
class NextWordPredictor(Resource):
    def get(self):
        global joker
        text = request.args.get('text')
        return joker.getCandidates(text, simTh=.001)

api.add_resource(JokeCompleter, '/complete_joke')
api.add_resource(NextWordPredictor, '/get_next_word')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=False, host='0.0.0.0', port=port)
