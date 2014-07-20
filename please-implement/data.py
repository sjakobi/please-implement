from collections import OrderedDict
import json
import re

from google.appengine.api import memcache
from agithub import Github
from config import username, password


CACHE_LONG = 60 * 60


def gh():
    return Github(username, password)


def exercism():
    return gh().repos.exercism


def get_exercises_in(repo, update=False):
    key = repo + '_exercises'
    exercises = memcache.get(key)

    if exercises is None or update:
        status, request = exercism()[repo].contents.get()
        if status == 200:
            all_exercises = get_all_exercises()
            exercises = {obj['name']
                         for obj in request
                         if obj['type'] == 'dir'
                         if obj['name'] in all_exercises}
            memcache.set(key, exercises, CACHE_LONG)

    return exercises


def get_unwanted_exercises_in(repo, update=False):
    """Return the set of exercises that are listed as "deprecated" or
    "ignored" in the config.json of the repo.
    The set may also contain the names of non-exercise directories in the
    repo.

    If update is True, fetch the config.json and update the memcache value.
    """
    key = repo + '_unwanted'
    unwanted = memcache.get(key)

    if unwanted is None or update:
        status, request = exercism()[repo].contents["config.json"].get()
        if status == 200:
            content = json.loads(request["content"].decode(request["encoding"]))
            unwanted = set(content["deprecated"] + content["ignored"])
            memcache.set(key, unwanted, CACHE_LONG)

    return unwanted


def get_all_exercises(update=False):
    exercises = memcache.get('all_exercises')

    if exercises is None or update:
        status, request = exercism()['x-common'].contents.get()
        if status == 200:
            exercises = {obj['name'][:-4]
                         for obj in request
                         if obj['name'].endswith('.yml')}
            memcache.set('all_exercises', exercises, CACHE_LONG)

    return exercises


def get_languages(update=False):
    languages = memcache.get('languages')

    if languages is None or update:
        status, request = gh().users.exercism.repos.get(per_page='100')
        if status == 200:
            repos = (obj['name']
                     for obj in request
                     if _is_language_repo(obj['name']))
            languages = OrderedDict((repo, get_real_language_name(repo))
                                    for repo in repos)
            memcache.set('languages', languages, CACHE_LONG)

    return languages


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


def _is_language_repo(repo):
    if not repo.lower().startswith("x"):
        return False
    status, request = exercism()[repo].contents["config.json"].get()
    if status != 200:
        return False
    content = json.loads(request["content"].decode(request["encoding"]))
    language = content.get("language", "")
    return language != ""
