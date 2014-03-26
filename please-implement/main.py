import webapp2

import table

class MainPage(webapp2.RequestHandler):
    def get(self):
        # show main overview of all exercises
        self.response.write("Hello, World!")


class Update(webapp2.RequestHandler):
    def get(self):
        table.update()
        # redirect back to /<language> if coming from there
        # maybe have /update/<language> for this?


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/update', Update)],
                              debug=True)
