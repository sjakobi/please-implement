import re
import time

#from google.appengine.api import memcache, urlfetch
from agithub import Github
from config import username, password


def update(language):
    pass


def update_all():
    pass


def courteously_do(f, *args, **kwargs):
    time.sleep(5)
    return f(*args, **kwargs)


def gh():
    return Github(username, password)


def exercism():
    return gh().repos.exercism


def get_exercises_in(repo):
    status, request = exercism()[repo].contents['EXERCISES.txt'].get()
    if status == 200:
        exercises = set(request['content'].decode(request['encoding']).split())
        return exercises
    # no EXERCISM.txt or other error
    status, request = exercism()[repo].contents.get()
    if status == 200:
        exercises = all_exercises()
        return {obj['name']
                for obj in request
                if obj['type'] == 'dir'
                if obj['name'] in exercises}


def all_exercises():
    status, request = exercism()['x-common'].contents.get()
    if status == 200:
        return {obj['name'][:-4]
                for obj in request
                if obj['name'].endswith('.yml')}


def get_language_list():
    status, request = gh().users.exercism.repos.get()
    if status == 200:
        return [obj['name']
                for obj in request
                if obj['name'].startswith('x')
                if not obj['name'].startswith('x-')]


def get_real_language_name(language_repo):
    status, request = exercism()[language_repo].readme.get()
    if status == 200:
        readme = request['content'].decode(request['encoding'])
        return _extract_language_name(readme)


def _extract_language_name(readme):
    match = re.search((r'Exercism [Ee]xercises in the ([^\n]+) '
                       '[Pp]rogramming [Ll]anguage\.?\n'),
                      readme)
    if not match:
        match = re.search(r'Exercism [Ee]xercises in ([^\n]+)\.?\n', readme)
    return match.group(1)
