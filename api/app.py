#!flask/bin/python
from flask import Flask, jsonify, request, make_response
import random
import final_hack
from time import sleep
from flask_cors import CORS


# from pymongo import MongoClient

app = Flask(__name__)
# app.run(port=3001)
CORS(app)

@app.route('/recommend', methods=['GET'])
def index():
    url = request.args.get('url')

    if (request.args.get('url')):
        resp = make_response(jsonify(final_hack.getRecommendations(url)))

    # if (request.cookies.get('_frc') is None):
    #     newCookie = random.randint(0,10000000000)
    #     resp.set_cookie('_frc', str(newCookie))
    
    return resp

if __name__ == '__main__':
    # app.run(debug=True, ssl_context=context)
    app.run(debug=True)
