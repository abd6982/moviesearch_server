from flask import Blueprint, request, g
import requests
import json
import os
import random
import string

movie_api = Blueprint('movie_api', __name__)


@movie_api.route("/search", methods=['POST'])
def search():
    data = json.loads(request.data)

    if 'query' not in data:
        return json.dumps({'result': 'Search Query not found in payload.'}), 400

    params = {
        's': data['query'],
        'type': 'movie',
        'apikey': g.OMDB_API_KEY
    }
    try:
        res = requests.get('http://www.omdbapi.com', params=params)
        search_results = json.loads(res.text)
        if search_results['Response'] == 'True':
            return json.dumps({'result': 'ok', 'data': search_results['Search']}), 200
        else:
            return json.dumps({'result': search_results['Error']}), 200

    except Exception as e:
        return json.dumps({'result': "server_error", "error": str(e)}), 500


@movie_api.route("/get", methods=['POST'])
def get():
    data = json.loads(request.data)

    if 'id' not in data or 'title' not in data or 'year' not in data:
        return json.dumps({'result': 'Insufficient data supplied.'}), 400

    omdb_params = {
        'i': data['id'],
        'apikey': g.OMDB_API_KEY
    }

    youtube_params = {
        'part': 'snippet',
        'maxResults': '5',
        'type': 'video',
        'q': data['title'] + ' ' + data['year'] + ' trailer',
        'key': g.YOUTUBE_V3_API_KEY
    }
    try:
        imdb_res = requests.get('http://www.omdbapi.com', params=omdb_params)
        movie_info = json.loads(imdb_res.text)
        youtube_res = requests.get('https://www.googleapis.com/youtube/v3/search', params=youtube_params)
        if movie_info['Response'] == 'True':
            return json.dumps({'result': 'ok', 'data': movie_info, 'videos': json.loads(youtube_res.text)}), 200
        else:
            return json.dumps({'result': movie_info['Error']}), 200

    except Exception as e:
        return json.dumps({'result': "server_error", "error": str(e)}), 500
