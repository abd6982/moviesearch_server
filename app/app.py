import os
import sys

from flask import Flask, g
from flask_cors import CORS
from dotenv import load_dotenv
import redis

from api.movie import movie_api

PATH = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(PATH)

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path, verbose=True)

PORT = int(os.getenv('PORT'))
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_CACHE_TIMEOUT = int(os.getenv('REDIS_CACHE_TIMEOUT'))
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
YOUTUBE_V3_API_KEY = os.getenv('YOUTUBE_V3_API_KEY')

app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


@app.before_request
def before_request_callback():
    g.OMDB_API_KEY = OMDB_API_KEY
    g.YOUTUBE_V3_API_KEY = YOUTUBE_V3_API_KEY
    g.redis = redis_client
    g.REDIS_CACHE_TIMEOUT = REDIS_CACHE_TIMEOUT


app.register_blueprint(movie_api, url_prefix='/api/movie')

if __name__ == '__main__':
    app.run(port=PORT, host="0.0.0.0")
