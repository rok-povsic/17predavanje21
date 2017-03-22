#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class ShraniHandler(BaseHandler):
    def post(self):
        sporocilo = self.request.get('sporocilo')
        ime = self.request.get("ime")

        # Shrani sporocilo v bazo.
        spr = Sporocilo(vnos=sporocilo, ime=ime)
        spr.put()

        return self.write("Shranjeno.")

class VsaSporocilaHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query().fetch()
        spremenljivke = {
            "sporocila": sporocila
        }
        return self.render_template("seznam.html", spremenljivke)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        return self.write(sporocilo.ime + " " + sporocilo.vnos)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/shrani', ShraniHandler),
    webapp2.Route('/vsa-sporocila', VsaSporocilaHandler),
    webapp2.Route(
        '/posamezno-sporocilo/<sporocilo_id:\d+>',
        PosameznoSporociloHandler),
], debug=True)
