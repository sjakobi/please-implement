import os

import jinja2
import webapp2

from data import get_exercises_in, get_all_exercises, get_languages
from table import front_table, table_for


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               extensions=['jinja2htmlcompress.HTMLCompress'],
                               autoescape=True)
TABLE_TEMPLATE = JINJA_ENV.get_template('table.html')


class Handler(webapp2.RequestHandler):

    def render(self, table):
        self.response.write(TABLE_TEMPLATE.render(zip=zip, table=table))


class TablePage(Handler):

    #TODO: validate repo
    def get(self, repo):
        table = table_for(repo.lower()) if repo else front_table()
        self.render(table)


class UpdatePage(webapp2.RequestHandler):

    #TODO: validate repo
    def get(self, repo):
        get_all_exercises(update=True)
        if repo:
            get_exercises_in(repo, update=True)
        else:
            for r in get_languages(update=True):
                get_exercises_in(r, update=True)

        self.redirect("/" + repo)


REGEX = r'([a-z0-9-]*)/?'
app = webapp2.WSGIApplication([(r'/update/?' + REGEX, UpdatePage),
                               (r'/' + REGEX, TablePage)],
                              debug=True)
