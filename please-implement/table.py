#from google.appengine.api import memcache, urlfetch
from collections import namedtuple

from data import (all_exercises, courteously_do, get_exercises_in,
                  get_language_list, get_real_language_name)


Table = namedtuple('Table', 'language column_names exercises rows')


def update():
    # get x-common
    # get list of languages
    # call update_lang() for all languages
    pass


def table_for(language):
    pass


def front_table():
    # needs to also handle exercises that shall not be implemented in
    # a given language
    exercises = sorted(all_exercises())
    languages = get_language_list()
    exercises_in = {lang: get_exercises_in(lang)
                    for lang in languages}
    real_language_names = [get_real_language_name(lang)
                           for lang in languages]
    rows = [[lang if (ex in exercises_in[lang]) else None
             for lang in languages]
            for ex in exercises]
    return Table(language=None,
                 column_names=real_language_names,
                 exercises=exercises,
                 rows=rows)
