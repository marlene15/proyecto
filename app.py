import os
import webapp2
import jinja2
import logging

from google.appengine.ext import db
from google.appengine.ext import ndb #Importa para usar la base de datos NDB
from webapp2_extras import sessions
from datetime import date #Para usar el formato de fecha

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):        
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw) 

#Creamos el modelo NDB, Contiene 4 entidades
class Cuentas(ndb.Model):
  "Models an individual Guestbook entry with content and date."
  username = ndb.StringProperty()
  password = ndb.StringProperty()

class Login(Handler):
    def get(self):
      self.render("loginscreen.html")
    
    def post(self):
      user = self.request.get("user")
      logging.info('POST user='+str(user))
      pw = self.request.get('password')
      logging.info('POST password='+str(pw))
      msg = ' '
      password = "marlene"
      if pw == '' or user == '':
          msg = 'Please specify Account and Password'
          self.render("loginscreen.html", error=msg)
      elif pw == password:
          msg = 'Bienvenido'
          self.render("index.html") 
      else:
        msg = 'Password incorrecto'
        self.render("loginscreen.html",error=msg)

class Index(Handler):
    def get(self):        
        self.render("index.html") 

class Categorias(Handler):
    def get(self):
      self.render("categorias.html")

class Reportes(Handler):
    def get(self):
      self.render("reportes.html")

class Salir(Handler):
    def get(self):
      self.render("salir.html")
    
app = webapp2.WSGIApplication([('/', Login),
                               ('/index', Index),                               
                               ('/categorias',Categorias),
                               ('/reportes',Reportes),
                               ('/salir',Salir)
                              ],
                              debug=True)