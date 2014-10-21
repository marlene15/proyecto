import os
import webapp2
import jinja2
import logging

from google.appengine.ext import db
from google.appengine.ext import ndb #Importa para usar la base de datos NDB
from webapp2_extras import sessions
import re #para expresiones regulares
from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def dispatch(self):
      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)
      try:
          # Dispatch the request.
          webapp2.RequestHandler.dispatch(self)
      finally:
          # Save all sessions.
          self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def render(self, template, **kw):        
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw) 

#Creamos el modelo NDB, Contiene 4 entidades
class Cuentas(ndb.Model):
  "Models an individual Guestbook entry with content and date."
  username = ndb.StringProperty()
  password = ndb.StringProperty()

#Propiedades de la estructura
class Usuario(ndb.Model):
  nombre = ndb.StringProperty()
  apellido = ndb.StringProperty()
  email = ndb.StringProperty()
  #fecha = ndb.DateProperty()
  sexo = ndb.StringProperty()
  cuenta=ndb.StructuredProperty(Cuentas) #Heredamos de la estructura de Cuentas

class Clientes(ndb.Model):
  nombre = ndb.StringProperty()
  apellidos = ndb.StringProperty()
  email = ndb.StringProperty()
  tel = ndb.StringProperty()

class MaquillajeM(ndb.Model):
  producto = ndb.StringProperty()
  descripcion = ndb.StringProperty()
  cantidad = ndb.StringProperty()
  cliente = ndb.StringProperty()
  precio_total = ndb.StringProperty()

class LineadecolorM(ndb.Model):
  producto = ndb.StringProperty()
  descripcion = ndb.StringProperty()
  cantidad = ndb.StringProperty()
  precio_total = ndb.StringProperty()

class Login(Handler):
    def get(self):
        self.render("loginscreen.html")    
    def post(self):
      user = self.request.get("user")
      pw = self.request.get('password')          
      msg = ' '
      if pw == '' or user == '':
        msg = 'Por favor especifique el usuario y la contrasena'
        self.render("loginscreen.html", error=msg)
      else:
        consulta=Usuario.query(ndb.AND(Usuario.cuenta.username==user, Usuario.cuenta.password==pw)).get()
        if consulta is not None:
          user = self.request.get('user')
          self.session['user'] = user
          logging.info("%s just logged in" % user)
          self.redirect('/index')
        else:
          msg = 'Usuario o contrasena incorrectos'
          self.render("loginscreen.html",error=msg)      

class Index(Handler):
    def get(self): 
        user = self.session.get('user')
        logging.info('Checkin index user value='+str(user))
        template_values={
            'user':user
            }
        self.render("index.html", user=template_values)       
        #self.render("index.html") 

class Maquillaje(Handler):
    def get(self):
      self.render("maquillaje.html")
      
class Maquillaje1(Handler):
    def get(self):
      # consulta = Clientes.query().fetch()
      # logging.info('Clientes: '+str(consulta))
      # registro = []
      # registro = consulta
      # logging.info('Registro: '+str(registro[1]))

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("maquillaje1.html",registro=registro2)

class Maquillaje2(Handler):
    def get(self):
      self.render("maquillaje2.html")

class Maquillaje3(Handler):
    def get(self):
      self.render("maquillaje3.html")      

class Lineadecolor(Handler):
    def get(self):
      self.render("lineadecolor.html")  

class Labios(Handler):
    def get(self):
      self.render("labios.html")  

class Labial1(Handler):
    def get(self):
      self.render("labial1.html")  

class Labial2(Handler):
    def get(self):
      self.render("labial2.html")  

class Ojos(Handler):
    def get(self):
      self.render("ojos.html")  

class Corrector(Handler):
    def get(self):
      self.render("corrector.html") 

class Sombras(Handler):
    def get(self):
      self.render("sombras.html") 

class Rimel(Handler):
    def get(self):
      self.render("rimel.html")              

class Delineador(Handler):
    def get(self):
      self.render("delineador.html")

class Lapiz(Handler):
    def get(self):
      self.render("lapiz.html")

class Mejillas(Handler):
    def get(self):
      self.render("mejillas.html")        

class Reportes(Handler):
    def get(self):
      self.render("reportes.html")

class Salir(Handler):
    def get(self):
        if self.session.get('user'):
            del self.session['user']
            self.redirect('/')

class Registra(Handler):
  def get(self):
        self.render("registrar.html")

class Registrar(Handler):
    def post(self):
        nombre = self.request.get('nombre')
        apellido = self.request.get('apellido')
        email = self.request.get('email')                
        user = self.request.get('user')
        pw = self.request.get('password')
        #fecha = self.request.get('fecha')
        sexo = self.request.get('sexo')

        if mail.is_email_valid(email):
          #Se crea uan entidad de tipos usuarios con propiedades estructuradas
          usuario=Usuario(nombre=nombre,
                          apellido=apellido,
                          email=email,
                          sexo=sexo,
                          cuenta=Cuentas(username=user,password=pw)
                          )
          #Se guarda la entidad de tipo usuario  con propiedades estructuradas
          usuario=usuario.put()
          #Obtengo la llave de la entidad de usuario
          usuariokey=usuario.get()          
          
          sender_address = "10460292@itcolima.edu.mx"
          subject = "Registro completo"
          body = "Gracias por registrarse"
          mail.send_mail(sender_address,email, subject, body)

          self.redirect('/')           
        else:
          self.render("registrar.html")    

class Registra_Cliente(Handler):  
    def get(self):
        self.render("clientes.html") 
    def post(self):
        nombre = self.request.get('nombre')
        apellidos = self.request.get('apellidos')
        email = self.request.get('email')                
        tel = self.request.get('telefono')

        # logging.info('nombre: '+str(nombre))
        # logging.info('apellidos: '+str(apellidos))
        # logging.info('email: '+str(email))
        # logging.info('tel: '+str(tel))

        clientes=Clientes(nombre=nombre,
                          apellidos=apellidos,
                          email=email,
                          tel=tel)
        #Se guarda la entidad de tipo clientes con propiedades estructuradas
        clientes=clientes.put()
        #Obtengo la llave de la entidad de clientes
        usuariokey=clientes.get()  
        self.redirect('/index') 

class Agrega_maquillaje(Handler):  
    def post(self):
      productos = self.request.get('productos', allow_multiple=True)
      descripcion = self.request.get('descripcion') 
      cantidades = self.request.get('cantidades', allow_multiple=True)
      precios = self.request.get('precios', allow_multiple=True)
      cliente = self.request.get('cliente', allow_multiple=True)
      
      logging.info('Tamanio del array:  '+str(len(cantidades)))

      logging.info('Descripcion: '+str(descripcion))
      logging.info('Cantidad en pa posicion 2: '+str(cantidades))

      #Se coloca el while para agregar todos los datos que se agregaron en la tabla
      indice=0
      while indice < len(cantidades):
        maquillajem=MaquillajeM(producto=productos[indice],
                            descripcion=descripcion,
                            cantidad=cantidades[indice],
                            cliente=cliente[indice],
                            precio_total=precios[indice])
        #Se guarda la entidad de tipo clientes con propiedades estructuradas
        maquillajem=maquillajem.put()
        indice += 1 
      self.render("maquillaje.html")
      #self.redirect('/maquillaje1') 

class Agregar_lineadecolor(Handler):
  def post(self):
      productos = self.request.get('productos', allow_multiple=True)
      descripcion = self.request.get('descripcion') 
      cantidades = self.request.get('cantidades', allow_multiple=True)
      precios = self.request.get('precios', allow_multiple=True)
      
      logging.info('Tamanio del array:  '+str(len(cantidades)))

      logging.info('Descripcion: '+str(descripcion))
      logging.info('Cantidad en pa posicion 2: '+str(cantidades))

      #Se coloca el while para agregar todos los datos que se agregaron en la tabla
      indice=0
      while indice < len(cantidades):
        lineadecolorm=LineadecolorM(producto=productos[indice],
                            descripcion=descripcion,
                            cantidad=cantidades[indice],
                            precio_total=precios[indice])
        #Se guarda la entidad de tipo clientes con propiedades estructuradas
        lineadecolorm=lineadecolorm.put()
        indice += 1 
      self.render("lineadecolor.html")

config = {}
config['webapp2_extras.sessions'] = {
  'secret_key': 'some-secret-key',
}

    
app = webapp2.WSGIApplication([('/', Login),
                               ('/index', Index),                               
                               ('/maquillaje',Maquillaje),
                               ('/maquillaje1',Maquillaje1),
                               ('/maquillaje2',Maquillaje2),                               
                               ('/maquillaje3',Maquillaje3),                               
                               ('/lineadecolor',Lineadecolor),                                                              
                               ('/labios',Labios),
                               ('/labial1',Labial1),
                               ('/labial2',Labial2),                               
                               ('/ojos',Ojos),
                               ('/sombras',Sombras),
                               ('/rimel',Rimel),
                               ('/delineador',Delineador),
                               ('/lapiz',Lapiz),
                               ('/corrector',Corrector),                                                                                                                                                                                          
                               ('/mejillas',Mejillas),                                                                                             
                               ('/reportes',Reportes),
                               ('/salir',Salir),
                               ('/registra',Registra),
                               ('/registrar',Registrar),
                               ('/clientes',Registra_Cliente),
                               ('/agrega_maquillaje',Agrega_maquillaje),
                               ('/agregar_lineadecolor',Agregar_lineadecolor)
                              ],
                              debug=True, config=config)