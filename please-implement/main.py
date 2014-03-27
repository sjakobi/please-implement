import os
from logging import warning

import jinja2
import webapp2

from table import front_table, table_for
from data import update, update_all


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)
TABLE_TEMPLATE = JINJA_ENV.get_template('table.html')


class Handler(webapp2.RequestHandler):

    def render(self, table):
        self.response.write(TABLE_TEMPLATE.render(zip=zip, table=table))


class TablePage(Handler):

    def get(self, language):
        #warning('tablepage, language=' + repr(language))
        if not language:
            language = ''
        if language:
            self.response.write('page for ' + repr(language))
        else:
            table = front_table()
            #self.response.write(repr(table))
            self.render(table)

        # validate language here?
        #if not language:
        #    self.render(front_table())
        #self.render(table_for(language))


class UpdatePage(webapp2.RequestHandler):

    def get(self, language=None):
        #warning('updatepage, language=' + repr(language))
        if not language:
            language = ''

        if not language:
            update_all
        else:   # handle unknown languages?
            update(language)
        self.redirect('/' + language)


REGEX = r'([a-z0-9-]*)/?'
app = webapp2.WSGIApplication([('/update/' + REGEX, UpdatePage),
                               (r'/' + REGEX, TablePage)],
                              debug=True)
