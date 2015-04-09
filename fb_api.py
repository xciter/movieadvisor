__author__ = 'i.yesilevsky'
import json
import urllib.parse
import urllib.request


def get_params():
    """
    Fulfilling parameters (limit and API KEY) for GET request.
    For detailed information of query refer to https://developers.facebook.com/docs/graph-api/reference/

    :return: parameters for GET request
    """
    access_token = 'Your access token'  # change to your access token
    params = {
        'access_token': access_token,
        'limit': 500
    }
    return params


def request_api():
    """
    Send request to API and return response results

    :return: response data in JSON format
    """
    # request the API and return results
    service_url = 'https://graph.facebook.com/me/video.watches'
    url = service_url + '?' + urllib.parse.urlencode(get_params())
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    return response['data']


def get_movies():
    """
    Get titles of popular movies from API request.

    :return: list of movies titles
    """
    movie_titles = []
    for movie in request_api():
        movie_titles.append(movie['data']['movie']['title'])
    return movie_titles
