from collections import namedtuple

from data import (get_all_exercises, get_exercises_in, get_languages,
                  get_unwanted_exercises_in)


Table = namedtuple('Table', 'repo languages rows exercises')


def table_for(repo):
    all_exercises = get_all_exercises()
    repo2real_name = get_languages()
    exercises = {repo: get_exercises_in(repo)
                 for repo in repo2real_name}
    rows = sorted((all_exercises
                   - exercises[repo]
                   - get_unwanted_exercises_in(repo)),
                  key=lambda ex: sum(ex in implemented
                                     for (r, implemented) in exercises.items()
                                     if r != repo),
                  reverse=True)
    return Table(repo=repo,
                 languages=repo2real_name,
                 rows=rows,
                 exercises=exercises)


def front_table():
    repo2real_name = get_languages()
    exercises = {repo: get_exercises_in(repo)
                 for repo in repo2real_name}
    rows = sorted(get_all_exercises(),
                  key=lambda x: sum(x in implemented
                                    for (r, implemented) in exercises.items()))
    return Table(repo=None,
                 languages=repo2real_name,
                 rows=rows,
                 exercises=exercises)
