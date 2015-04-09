__author__ = 'i.yesilevsky'
from pymongo import MongoClient


def add_to_mongo(movies):
    """
    Add list to MongoDB collection.
    You can change MongoDB and collection name.

    :param movies: list of movies information
    """
    try:
        client = MongoClient()
        db = client.movies_freebase
        collect = db.movies
        mov_id = collect.insert(movies)
    except Exception as exp:
        print(exp)
