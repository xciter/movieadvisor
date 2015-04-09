__author__ = 'i.yesilevsky'
import json
import urllib.parse
import urllib.request


def get_params(page):
    """
    Fulfilling parameters (page and API KEY) for GET request.
    For detailed information of query refer to http://docs.themoviedb.apiary.io/

    :param page: page number to iterate response
    :return: parameters for GET request
    """
    api_key = 'Your API key'  # change this to your API key
    params = {
        'Accept': 'application/json',
        'api_key': api_key,
        'page': page
    }
    return params


def request_api(page):
    """
    Send request to API for specific page and return response results

    :param page: page number
    :return: response results in JSON format
    """
    # request the API for specific page and return results
    service_url = 'http://api.themoviedb.org/3/movie/popular'
    url = service_url + '?' + urllib.parse.urlencode(get_params(page))
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    return response['results']


def get_movies():
    """
    Get titles of popular movies from API request.

    :return: list of movies titles
    """
    movie_titles = []
    for page in range(1, 20):  # I've chosen first 20 pages
        for movie in request_api(page):
            movie_titles.append(movie['title'])
    return movie_titles