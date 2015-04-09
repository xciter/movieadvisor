__author__ = 'i.yesilevsky'
import json
import urllib.parse
import urllib.request
import time

from db_connector import add_to_mongo


def get_params(cursor_value):
    """
    Fulfilling parameters (MQL query, cursor value and API KEY) for GET request.
    For detailed information of query refer to https://developers.google.com/freebase/v1/mql-overview

    :param cursor_value: value of cursor to iterate response results
    :return: parameters for GET request
    """
    api_key = 'Your API key'  # change this to your API key from https://console.developers.google.com/project

    query = [{
        "id": None,
        "name": None,
        "ru:name": {
            "lang": "/lang/ru",
            "value": None
        },
        "initial_release_date": None,
        "genre": [],
        "country": [],
        "directed_by": [],
        "starring": [{
            "actor": None
        }],
        "type": "/film/film",
        "limit": 500
    }]

    params = {
        'key': api_key,
        'query': json.dumps(query),
        'cursor': cursor_value
    }
    return params


def request_api(cursor):
    """
    Send request to API and return response

    :param cursor: value of cursor to get information from specific page
    :return: response in JSON format
    """
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    url = service_url + '?' + urllib.parse.urlencode(get_params(cursor))
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    return response


def get_movies(response_result):
    """
    Get information about movies from API response and fill it in needed form.

    :param response_result: response in JSON format
    :return:
    """
    movies_info = []
    for movie in response_result:
        movie_info = {
            'movie_id': movie['id'],
            'title': movie['name'],
            'alt_title': movie['ru:name']['value'],
            'year': movie['initial_release_date'],
            'genres': movie['genre'],
            'countries': movie['country'],
            'director': movie['directed_by'],
            'actors': list(stars['actor'] for stars in movie['starring'])
        }
        movies_info.append(movie_info)
    return movies_info


def make_db():
    """
    Send request to API and get needed information. After add it to MongoDB collection.
    """
    response = request_api('')  # First request should contain empty cursor value
    movie_list = []
    while response['cursor']:  # for last page with information cursor will be False
        movie_list.extend(get_movies(response['result']))
        print(len(movie_list))
        if len(movie_list) >= 10000:
            add_to_mongo(movie_list)
            movie_list = []
        try:
            response = request_api(response['cursor'])
        except Exception as exp:
            print(exp)

    add_to_mongo(movie_list)


def start_api():
    """
    Method for debugging. It measures elapsed time to create database
    """
    start = time.clock()
    make_db()
    end = time.clock()
    print('time elapsed:', str(end-start))

