import os
from google.appengine.ext.webapp import template
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class VendorApp(db.Model):
    author = db.UserProperty()
    boothname = db.StringProperty()
    type = db.StringProperty(choices=set(["food", "arts1", "arts2" "info"]))
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
        template_values = { 'greeting': greeting }
        
        path = os.path.join(os.path.dirname(__file__), 'apply.html')
        self.response.out.write(template.render(path, template_values))

class VendorApplication(webapp.RequestHandler):
    def post(self):
        vendorapp = VendorApp()

        if users.get_current_user():
            vendorapp.author = users.get_current_user()

        vendorapp.boothname = self.request.get('boothname')
        vendorapp.type = self.request.get('type')
        vendorapp.put()
        self.redirect('/thankyou')

class ThankYou(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'thankyou.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/apply', VendorApplication),
                                      ('/thankyou', ThankYou)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()