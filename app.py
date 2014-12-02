import os
import webapp2
import jinja2
import logging
import datetime
import Crypto

from google.appengine.ext import db
from google.appengine.ext import ndb #Importa para usar la base de datos NDB
from webapp2_extras import sessions
import re #para expresiones regulares
from google.appengine.api import mail
from Crypto.Hash import SHA256 #encriptar contrasenia

#uso de OAuth
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator

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
  dire = ndb.StringProperty()

class MaquillajeM(ndb.Model):
  producto = ndb.StringProperty()
  descripcion = ndb.StringProperty()
  cantidad = ndb.StringProperty()
  cliente = ndb.StringProperty()
  precio_total = ndb.StringProperty()
  fecha = ndb.DateProperty()

class LineadecolorM(ndb.Model):
  producto = ndb.StringProperty()
  descripcion = ndb.StringProperty()
  cantidad = ndb.StringProperty()
  cliente = ndb.StringProperty()
  precio_total = ndb.StringProperty()
  fecha = ndb.DateProperty()

class ProductosMaquillajes(ndb.Model):
  categoria = ndb.StringProperty()
  producto = ndb.StringProperty()
  precios = ndb.StringProperty()

class ProductosLinea(ndb.Model):
  categoria = ndb.StringProperty()
  subcategoria = ndb.StringProperty()
  producto = ndb.StringProperty()
  precios = ndb.StringProperty()

class Login(Handler):
    def get(self):
        self.render("loginscreen.html")    
    def post(self):
      user = self.request.get("user")
      pw = self.request.get('password')    
      pw = SHA256.new(pw).hexdigest()   
      #logging.info('pw'+str(pw))   
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
      saludo = self.request.get('m')
      logging.info('Saludo: '+str(saludo))      

      productos=ProductosMaquillajes.query()
      prod_m=[]
      prod_m=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("maquillaje1.html",registro=registro2,productos=prod_m)

class Maquillaje2(Handler):
    def get(self):
      productos=ProductosMaquillajes.query()
      prod_m=[]
      prod_m=productos

      consulta=Clientes.query()
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("maquillaje2.html",registro=registro2,productos=prod_m)

class Maquillaje3(Handler):
    def get(self):
      productos=ProductosMaquillajes.query()
      prod_m=[]
      prod_m=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("maquillaje3.html",registro=registro2,productos=prod_m)

class Lineadecolor(Handler):
    def get(self):
      self.render("lineadecolor.html")  

class Labios(Handler):
    def get(self):
      self.render("labios.html")  

class Labial1(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Labios', ProductosLinea.subcategoria=='Lapiz labial true dimensions'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("labial1.html",registro=registro2,productos=prod_l)

class Labial2(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Labios', ProductosLinea.subcategoria=='Brillo labial Nourishine'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("labial2.html",registro=registro2,productos=prod_l)

class Ojos(Handler):
    def get(self):
      self.render("ojos.html")  

class Corrector(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Ojos', ProductosLinea.subcategoria=='Corrector para ojos'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("corrector.html",registro=registro2,productos=prod_l)
      
class Sombras(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Ojos', ProductosLinea.subcategoria=='Sombras mineral compacta'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("sombras.html",registro=registro2,productos=prod_l)

class Rimel(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Ojos', ProductosLinea.subcategoria=='Mascara para pest'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("rimel.html",registro=registro2,productos=prod_l)
        
class Delineador(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Ojos', ProductosLinea.subcategoria=='Delineador de ojos'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("delineador.html",registro=registro2,productos=prod_l)

class Lapiz(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Ojos', ProductosLinea.subcategoria=='Lapiz delineador para ojos'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("lapiz.html",registro=registro2,productos=prod_l)

class Mejillas(Handler):
    def get(self):
      productos=ProductosLinea.query(ndb.AND(ProductosLinea.categoria=='Mejillas', ProductosLinea.subcategoria=='Ninguna'))
      prod_l=[]
      prod_l=productos

      consulta=Clientes.query()
      for result in consulta.iter():
           logging.info("result:" + str(result))
      registro2=[]
      registro2=consulta
      logging.info("registro2:" + str(registro2))
      self.render("mejillas.html",registro=registro2,productos=prod_l)
            
class Reportes(Handler):
    def get(self):
      clientes=Clientes.query()  
      clie_l=[]
      clie_l=clientes
      self.render("reportes.html", clientes=clie_l)

class Salir(Handler):
    def get(self):
        if self.session.get('user'):
            del self.session['user']
            self.redirect('/')

class Productos(Handler):
  def get(self):
        self.render("productos.html")

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
        pw = SHA256.new(pw).hexdigest()
        #logging.info("pw:" + str(pw))
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
          
          sender_address = "sn.equipo1@gmail.com"
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
        dire = self.request.get('direccion')

        clientes=Clientes(nombre=nombre.lower(), #Guarda en minuscula
                          apellidos=apellidos.lower(),
                          email=email,
                          tel=tel,
                          dire=dire)
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

      # logging.info('Tamanio del array:  '+str(len(cantidades)))
      # logging.info('Descripcion: '+str(descripcion))
      # logging.info('Cantidad en pa posicion 2: '+str(cantidades))

      #Se coloca el while para agregar todos los datos que se agregaron en la tabla
      indice=0
      while indice < len(cantidades):
        maquillajem=MaquillajeM(producto=productos[indice],
                            descripcion=descripcion,
                            cantidad=cantidades[indice],
                            cliente=cliente[indice],
                            precio_total=precios[indice],
                            fecha=datetime.date.today())
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
      cliente = self.request.get('cliente', allow_multiple=True)
      
      # logging.info('Tamanio del array:  '+str(len(cantidades)))
      # logging.info('Descripcion: '+str(descripcion))
      # logging.info('Cantidad en pa posicion 2: '+str(cantidades))

      #Se coloca el while para agregar todos los datos que se agregaron en la tabla
      indice=0
      while indice < len(cantidades):
        lineadecolorm=LineadecolorM(producto=productos[indice],
                            descripcion=descripcion,
                            cantidad=cantidades[indice],
                            cliente=cliente[indice],
                            precio_total=precios[indice],
                            fecha=datetime.date.today())
        #Se guarda la entidad de tipo clientes con propiedades estructuradas
        lineadecolorm=lineadecolorm.put()
        indice += 1 
      self.render("lineadecolor.html")

#REPORTE CATALOGO DE ARTICULOS
class producto_maquillaje(Handler):
    def post(self):
      maquillaje = self.request.get('maquillaje', allow_multiple=True)
      producto = self.request.get('producto1')
      precios = self.request.get('precios1')

      if maquillaje[0] == 'Maquillaje Liquidon Cobertura Media':
        maquillaje='MLCM'
      else: 
        if maquillaje[0] == 'Maquillaje en Polvo Suelto Mineral':
          maquillaje = 'MPSM'
        else:
          if maquillaje[0] == 'Maquillaje en Polvo Cremoso':
            maquillaje = 'MPC'
      
      #Agrega a la base de datos
      maquillaje=ProductosMaquillajes(categoria=maquillaje,producto=producto, precios=precios)
      #Se guarda la entidad de tipo clientes con propiedades estructuradas
      maquillaje=maquillaje.put()
      self.render("productos.html")

class producto_linea(Handler):
    def post(self):
      categoria = self.request.get('categoria')
      subcategoria = self.request.get('subcategoria')
      producto = self.request.get('producto2')
      precios = self.request.get('precios2')
      #Agrega a la base de datos
      productos=ProductosLinea(categoria=categoria,subcategoria=subcategoria,producto=producto, precios=precios)
      #Se guarda la entidad de tipo clientes con propiedades estructuradas
      productos=productos.put()
      self.render("productos.html")
      # logging.info('categoria:  '+str(categoria))
      # logging.info('subcategoria:  '+str(subcategoria))
      # logging.info('producto:  '+str(producto))
      # self.render("productos.html")

#REPORTE DE ARTICULOS VENDIDOS
class producto_maquillajev(Handler):
    def post(self):
      maquillaje = self.request.get('maquillaje', allow_multiple=True)
      producto = self.request.get('producto')
      precios = self.request.get('precios')

      if maquillaje[0] == 'Maquillaje Liquidon Cobertura Media':
        maquillaje='MLCM'
      else: 
        if maquillaje[0] == 'Maquillaje en Polvo Suelto Mineral':
          maquillaje = 'MPSM'
        else:
          if maquillaje[0] == 'Maquillaje en Polvo Cremoso':
            maquillaje = 'MPC'
      
      #Agrega a la base de datos
      maquillaje=MaquillajeM(categoria=maquillaje,producto=producto, precios=precios)
      #Se guarda la entidad de tipo clientes con propiedades estructuradas
      maquillaje=maquillaje.put()
      self.render("productos.html")

class producto_lineav(Handler):
    def post(self):
      categoria = self.request.get('categoria')
      subcategoria = self.request.get('subcategoria')
      producto = self.request.get('producto')
      precios = self.request.get('precios')
      #Agrega a la base de datos
      productos=LineadecolorM(categoria=categoria,subcategoria=subcategoria,producto=producto, precios=precios)
      #Se guarda la entidad de tipo clientes con propiedades estructuradas
      productos=productos.put()
      self.render("productos.html")

class genera_reporte(Handler):
  def post(self):
    categoria = self.request.get('categoria')
    reporte = self.request.get('reporte')
    cliente = self.request.get('clientes')
    logging.info('cliente:  '+str(cliente))

    if reporte == '1' and categoria == '1':
       productos=ProductosMaquillajes.query()  
       prod_l=[]
       prod_l=productos
       self.render("articulosM.html", productos=prod_l)

    if reporte == '1' and categoria == '2':
       productos=ProductosLinea.query()  
       prod_l=[]
       prod_l=productos
       self.render("articulosL.html", productos=prod_l)

    if reporte == '2' and categoria == '1':
       productos=MaquillajeM.query()  
       prod_l=[]
       prod_l=productos
       self.render("articulosM2.html", productos=prod_l)   

    if reporte == '2' and categoria == '2':
       productos=LineadecolorM.query()  
       prod_l=[]
       prod_l=productos
       self.render("articulosL2.html", productos=prod_l)

    if reporte == '3':
       clientes=Clientes.query()  
       clie_l=[]
       clie_l=clientes
       self.render("ClientesR.html", clientes=clie_l)       

    if reporte == '4' and categoria =='1':
      cliente=MaquillajeM.query(MaquillajeM.cliente==cliente)
      ventas=[]
      ventas=cliente
      self.render("ventaclienteM.html", cliente=ventas)

    if reporte == '4' and categoria =='2':
      cliente=LineadecolorM.query(LineadecolorM.cliente==cliente)
      ventas=[]
      ventas=cliente
      self.render("ventaclienteL.html", cliente=ventas)  

    cantidad_totalM=0
    cantidad_totalL=0
    if reporte == '5':
      ventasM=MaquillajeM.query()    
      ventasL=LineadecolorM.query()
      ventas1=[]
      ventas2=[]
      ventas1=ventasM
      ventas2=ventasL

      for result1 in ventasM.iter():
        cantidad_totalM=cantidad_totalM+int(result1.precio_total)
      for result2 in ventasL.iter():
        cantidad_totalL=cantidad_totalL+int(result2.precio_total)
      ganancias=cantidad_totalM+cantidad_totalL
      self.render("ventas_totales.html", ventas1=ventas1,ventas2=ventas2,ganancias=ganancias) 

#---------------------OAuth2Decorator-------------------------------
decorator = OAuth2Decorator(
    client_id ='38744844939-31gg4resp8aqnkn9kkj7vm52pp9kv5bf.apps.googleusercontent.com',
    client_secret='aZT5bhCqKZY9Kwpai3zriojo',
    scope='https://www.googleapis.com/auth/calendar')
service = build('calendar','v3')   

class calendar(Handler):
  @decorator.oauth_required
  def get(self):
        items=[] 
        page_token = None
        while True:
          events = service.events().list(calendarId='primary', pageToken=page_token).execute(http=decorator.http())
          for event in events['items']:
            items = events.get('items',[])
          page_token = events.get('nextPageToken')
          if not page_token:
            break       
        self.render("calendar.html", response=items)

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
                               ('/productos',Productos),
                               ('/registrar',Registrar),
                               ('/clientes',Registra_Cliente),
                               ('/agrega_maquillaje',Agrega_maquillaje),
                               ('/agregar_lineadecolor',Agregar_lineadecolor),
                               ('/producto_maquillaje',producto_maquillaje),
                               ('/producto_linea',producto_linea),
                               ('/producto_maquillajev',producto_maquillajev),
                               ('/producto_lineav',producto_lineav),
                               ('/genera_reporte',genera_reporte),
                               ('/calendar',calendar),
                               (decorator.callback_path, decorator.callback_handler())
                              ],
                              debug=True, config=config)