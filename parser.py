__author__ = 'i.yesilevsky'
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

from db_connector import add_to_mongo


def load_page(movie_id):
    """
    Load WEB page with given movie_id and returning parsed information

    :param movie_id: ID of movie on WEB service
    :return: parsed movie information from parse_page() method
    """
    try:
        url = 'Enter your URL'  # Change this to URL of desired web service
        http = urlopen(url+str(movie_id))
        charset = http.info().get_param('charset')
        soup = BeautifulSoup(http.read(), from_encoding=charset)
        return parse_page(soup, movie_id)
    except Exception:
        print('Movie with id', movie_id, 'was not found')
        return None


def parse_page(soup, movie_id):
    """
    Parse Beautiful soup object to extract needed information and returning dictionary with movie info.
    Attributes of your WEB service page could differ

    :param soup: BS object of movie WEB page
    :param movie_id: ID of movie on WEB service
    :return: dictionary with movie info
    """
    title = soup.find(attrs={'itemprop': 'name'}).string
    alt_title = soup.find(attrs={'itemprop': 'alternateName'}).string
    year = soup.find(name='small').a.string
    genres = list(genre.string for genre in soup.find_all(attrs={'itemprop': 'genre'}))
    countries = list(a.string for a in soup.find(attrs={'class': 'main'}).find_all('a') if not a.get('itemprop'))
    description = soup.find(attrs={'itemprop': 'description'}).contents[0].strip()
    director = soup.find(id='directors').find(attrs={'class': 'person'}).string
    actors = list(actor.string for actor in soup.find(id='actors').find_all(attrs={'class': 'person'}))
    imdb = soup.find(attrs={'class': 'rating'}).string
    tags = 'No tags'
    if soup.find(id='tags'):
        tags = list(tag.string for tag in soup.find(id='tags').find_all('a'))
    poster_link = soup.find(attrs={'class': 'posterbig'}).find(name='img').get('src')

    movie_info = {
        'movie_id': movie_id,
        'title': title,
        'alt_title': alt_title,
        'year': year,
        'genres': genres,
        'countries': countries,
        'description': description,
        'director': director,
        'actors': actors,
        'imdb': imdb,
        'poster_link': poster_link
    }

    if tags is not 'No tags':
        movie_info['tags'] = tags

    return movie_info


def make_db():
    """
    Creating list with movies information and then add it to MongoDB collection.
    Range of WEB pages from your service could differ.
    This logic is just for iterating each page in range from 1 to 100000
    """
    movie_list = []
    for idx in range(1, 100000):  # 100000 is the number of last movie_id
        movie = load_page(idx)
        print(movie)
        if movie is not None:
            movie_list.append(load_page(idx))
    add_to_mongo(movie_list)
    print(len(movie_list))


def start_scrapping():
    """
    Method for debugging. It measures elapsed time to create database
    """
    start = time.clock()
    make_db()
    end = time.clock()
    print('time elapsed:', str(end-start))
