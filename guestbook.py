import jinja2
import os
import webapp2


from webapp2_extras import json
from google.appengine.api import users
from google.appengine.ext import ndb


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name='default_guestbook'):
    return ndb.Key('Guestbook', guestbook_name)

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    vote = ndb.IntegerProperty(default=0)

class MainPage(webapp2.RequestHandler):
    def get(self):
        greetings_query = Greeting.query(ancestor=guestbook_key()).order(-Greeting.vote)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Sign in'

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(greetings=greetings,
                                                url=url,
                                                url_linktext=url_linktext))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        greeting = Greeting(parent=guestbook_key())

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put() 
        self.redirect('/')

class AjaxHandler(webapp2.RequestHandler):
    def post(self):
        act = self.request.get('act') #action
        uid = self.request.get('uid') #unique comment id

        print act + "called by " + uid
        ret = None

        action_method = getattr(self, "act_" + act) #change to act
        ret = action_method()

        json_str = json.encode(ret)
        self.response.write(json_str)

    def act_upvote(self):
        temp_value = self.request.get('uid')
        return {"act": "upvote", "resp": temp_value}
        
    def act_downvote(self):
        temp_value = self.request.get('uid')
        return {"act": "downvote", "resp": temp_value}

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/ajax', AjaxHandler),
], debug=True)
