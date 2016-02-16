#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "daniel"
__date__ = "$06-mar-2012 16:06:23$"

import gtk
import Widgets
import datetime
import os
import gobject
import Chrome
import json
import re
if os.name != 'nt':
    import sh

libros = [
    ['Génesis', '^ge(?: nesis)??', 'Gn', '', []],
    ['Éxodo', '^ex(?: odo)?', 'Ex', '', []],
    ['Levítico', '^le(?: itico)?', 'Lv', '', []],
    ['Números', '^nu(?: meros)?', 'Nm', '', []],
    ['Deuteronomio', '^de(?: uteronomio)?', 'Dt', '', []],
    ['Josué', '^jos(?: sue)?', 'Jos', '', []],
    ['Jueces', '^jue(?: ces)?', 'Judg', '', []],
    ['Rut', '^ru(?: t)?', 'Ruth', '', []],
    ['1 Samuel', '^1s(?: amuel)?', '1S', '', []],
    ['2 Samuel', '^2s(?: amuel)?', '2S', '', []],
    ['1 Reyes', '^1r(?: eyes)?', '1Ki', '', []],
    ['2 Reyes', '^2r(?: eyes)?', '2Ki', '', []],
    ['1 Crónicas', '^1cr(?: onicas)?', '1Chr', '', []],
    ['2 Crónicas', '^2cr(?: onicas)?', '2Chr', '', []],
    ['Esdras', '^esd(?: ras)?', 'Ezra', '', []],
    ['Nehemías', '^ne(?: hemias)?', 'Neh', '', []],
    ['Ester', '^est(?: er)?', 'Est', '', []],
    ['Job', '^jo(?: b)?', 'Jb', '', []],
    ['Salmos', '^sal( ?:)?mos', 'Psal', '', []],
    ['Proverbios', '^pr(?: verbios)?', 'Pr', '', []],
    ['Eclesiastés', '^ec(?: lesiastes)?', 'Ec', '', []],
    ['Cantar de los Cantares', '^ca(?: ntares)?', 'Song', '', []],
    ['Isaías', '^i(?: saias)?', 'Is', '', []],
    ['Jeremías', '^je(?: remias)?', 'Jr', '', []],
    ['Lamentaciones', '^la(?: mentaciones)?', 'La', '', []],
    ['Ezequiel', '^ez(?: equiel)?', 'Ez', '', []],
    ['Daniel', '^da(?: niel)?', 'Dn', '', []],
    ['Oseas', '^o(?: seas)?', 'Hos', '', []],
    ['Joel', '^joe(?: el)?', 'Jl', '', []],
    ['Amós', '^am(?: os)?', 'Am', '', []],
    ['Abdías', '^ab(?: dias)?', 'Obad', '', []],
    ['Jonás', '^jon(?: as)?', 'Jon', '', []],
    ['Miqueas', '^mi(?: queas)?', 'Mic', '', []],
    ['Nahúm', '^na(?: hum)?', 'Na', '', []],
    ['Habacuc', '^hab(?: bacuc)?', 'Hab', '', []],
    ['Sofonías', '^so(?: fonias)?', 'So', '', []],
    ['Hageo', '^hag(?: eo)?', 'Hag', '', []],
    ['Zacarías', '^z(?: acarias)?', 'Zech', '', []],
    ['Malaquías', '^mal(?: aquias)?', 'Ml', '', []],
    ['Mateo', '^mat(?: eo)?', 'Mt', '', []],
    ['Marcos', '^mar(?: cos)?', 'Mr', '', []],
    ['Lucas', '^lu(?: cas)?', 'Lu', '', []],
    ['Juan', '^jua(?: n)?', 'Jn', '', []],
    ['Hechos de los Apóstoles', '^hec(?: hos)?', 'Acts', '', []],
    ['Romanos', '^ro(?: manos)?', 'Ro', '', []],
    ['1 Corintios', '^1co(?: rintios)?', '1Co', '', []],
    ['2 Corintios', '^2co(?: rintios)?', '2Co', '', []],
    ['Gálatas', '^ga(?: latas)?', 'Gal', '', []],
    ['Efesios', '^ef(?: esios)?', 'Eph', '', []],
    ['Filipenses', '^fili(?: penses)?', 'Phil', '', []],
    ['Colosenses', '^co(?: losenses)?', 'Col', '', []],
    ['1 Tesalonicenses', '^1te(?: esalonicenses)?', '1Thess', '', []],
    ['2 Tesalonicenses', '^2te(?: esalonicenses)?', '2Thess', '', []],
    ['1 Timoteo', '^1ti(?: moteo)?', '1Tim', '', []],
    ['2 Timoteo', '^2ti(?: moteo)?', '2Tim', '', []],
    ['Tito', '^t(?: ito)?', 'Tt', '', []],
    ['Filemón', '^file(?: mon)?', 'Phlm', '', []],
    ['Hebreos', '^heb(?: reos)?', 'Hb', '', []],
    ['Santiago', '^san(?: tiago)?', 'Jas', '', []],
    ['1 Pedro', '^1p(?: edro)?', '1P', '', []],
    ['2 Pedro', '^2p(?: edro)?', '2P', '', []],
    ['1 Juan', '^1j(?: uan)?', '1Jn', '', []],
    ['2 Juan', '^2j(?: uan)?', '2Jn', '', []],
    ['3 Juan', '^3j(?: uan)?', '3Jn', '', []],
    ['Judas', '^jud(?: as)?', 'Jd', '', []],
    ['Apocalipsis', '^ap(?: ocalipsis)?', 'Rev', '', []],
]

class Ventana(gtk.Window):

    __gsignals__ = {'cerrar': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ()),
            'login': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ()),
            'salidas': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ())
        }

    def __init__(self, principal, version, dia):
        self.version = version
        super(Ventana, self).__init__()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/fondo-salida.jpg")
        pixmap, mask = pixbuf.render_pixmap_and_mask()
        width, height = pixmap.get_size()
        del pixbuf
        titulo = 'Sistema de Proyección %s' % version
        self.status_bar = Widgets.Statusbar()
        self.status_bar.push(dia)
        herramientas = [
            ('Sincronizar', 'sincronizar.png', self.sincronizar),
            ('Full Screen', 'fullscreen.png', self.fullscreen),
            ('Limpiar', 'limpiar.png', self.limpiar),
            ('Anterior', 'anterior.png', self.anterior),
            ('Siguiente', 'siguiente.png', self.siguiente),
            ('Fuente +', 'A+.png', self.mas_grande),
            ('Fuente -', 'A-.png', self.menos_grande),
            ]
        toolbar = Widgets.Toolbar(herramientas)
        ticketera = Widgets.Button('imprimir.png', '', 16)
        ticketera.connect('button-press-event', self.ticketera)
        self.menu = gtk.Menu()
        item2 = gtk.MenuItem('LPT1')
        item2.connect('activate', self.impresora_paralela)
        self.menu.append(item2)
        item3 = gtk.MenuItem('Probar')
        item3.connect('activate', self.impresora_probar)
        self.menu.append(item3)
        item4 = gtk.MenuItem('Reimprimir Último')
        item4.connect('activate', self.impresora_reimprimir)
        self.menu.append(item4)
        self.http = principal.http
        self.logueado = False
        self.set_app_paintable(gtk.TRUE)
        self.realize()
        self.window.set_back_pixmap(pixmap, gtk.FALSE)
        self.principal = principal
        #self.http = principal.http
        self.connect('destroy', self.cerrar)
        #Maquetación
        self.set_border_width(2)
        self.set_title(titulo)
        self.set_position(gtk.WIN_POS_CENTER)
        main_vbox = gtk.VBox(False, 0)
        path = os.path.join('images', 'icono.png')
        icon = gtk.gdk.pixbuf_new_from_file(path)
        self.set_icon_list(icon)
        #main_vbox.pack_start(toolbar, False, False, 0)

        self.add(main_vbox)
        self.toolbar = toolbar
        self.toolbar.add_button('Anterior (Ctrl + F)', 'izquierda.png', self.anterior)
        main_vbox.pack_start(self.toolbar, False, False, 0)
        hbox_main = gtk.HBox(False, 2)
        main_vbox.pack_start(hbox_main, True, True, 0)
            #VBox 1
        self.notebook = Widgets.Notebook()
        hbox_main.pack_start(self.notebook, True, True, 0)
        self.notebook.set_tab_pos(gtk.POS_TOP)
        musica_hbox = gtk.HBox(True, 0)
        self.notebook.insert_page(musica_hbox, gtk.Label('Música'))
        vbox1 = gtk.VBox(False, 0)
        musica_hbox.pack_start(vbox1, True, True, 0)
        self.notebook.set_homogeneous_tabs(True)
        self.notebook.child_set_property(musica_hbox, 'tab-expand', True)

        self.repertorio = Widgets.TreeViewId('Repertorio', ('NOMBRE', 'ALBUM', 'ARTISTA', 'ULTIMA', '*LETRAS'))
        vbox1.pack_start(self.repertorio, True, True, 0)
        self.repertorio.scroll.set_size_request(200, 400)
        self.seleccionados = Widgets.TreeViewId('Seleccionados', ('NOMBRE', 'ALBUM', 'ARTISTA', 'ULTIMA', '*LETRAS'))
        vbox1.pack_start(self.seleccionados, True, True, 0)
        self.seleccionados.scroll.set_size_request(200, 200)
            #VBox 2
        vbox2 = gtk.VBox(False, 0)
        musica_hbox.pack_start(vbox2, True, True, 0)
                #Notebook
        self.parrafos = Widgets.TreeViewId('Párrafos', ('LETRAS',))
        vbox2.pack_start(self.parrafos, True, True, 0)
        self.parrafos.scroll.set_size_request(200, 600)
                #Vueltas

        biblia_hbox = gtk.HBox(True, 0)
        self.notebook.insert_page(biblia_hbox, gtk.Label('Biblia'))
        vbox3 = gtk.VBox(False, 0)
        biblia_hbox.pack_start(vbox3, True, True, 0)
        frame = Widgets.Frame('Versículos')
        vbox = gtk.VBox(False, 0)
        self.version = Widgets.ComboBox()
        self.version.set_lista((('RVR60', 1),))
        vbox.pack_start(self.version, False, False, 0)
        self.entry_versiculo = Widgets.Texto(32)
        self.entry_versiculo.set_size_request(175, 25)
        self.entry_versiculo.connect('activate', self.buscar_versiculo)
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.entry_versiculo, False, False, 0)
        boton = Widgets.Button('mostrar.png', '', 24, self.mostrar_versiculo)
        hbox.pack_start(boton, False, False, 0)
        self.text_versiculo = Widgets.TextView()
        self.text_versiculo.set_size_request(200, 200)
        vbox.pack_start(self.text_versiculo, False, False, 0)
        frame.add(vbox)
        vbox3.pack_start(frame, False, False, 0)



            #VBox3
        vbox_fija = gtk.VBox(False, 0)
        hbox_main.pack_start(vbox_fija, False, False, 0)
        frame = Widgets.Frame('Vista Previa')
        if os.name == 'nt':
            url = 'local/proyeccion.html'
            self.vista_previa = Chrome.Browser(url, 200, 200)
            self.proyector  = Chrome.Window(url)
        else:
            url = 'file:///home/danielypamela/Python/Proyeccion/local/proyeccion.html'
            self.vista_previa = Chrome.IFrame(url, 200, 200)
            self.proyector = Chrome.Window(url)
        frame.add(self.vista_previa)
        vbox_fija.pack_start(frame, False, False, 0)
        frame = Widgets.Frame('Edición')
        vbox = gtk.VBox(False, 0)
        frame.add(vbox)
        self.text_mostrar = Widgets.TextView()
        self.text_mostrar.set_size_request(200, 200)
        vbox.pack_start(self.text_mostrar, False, False, 0)
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, False, False, 0)
        boton = Widgets.Button('mostrar.png', 'Mostrar', 24, self.mostrar_edicion)
        hbox.pack_start(boton, False, False, 0)
        boton = Widgets.Button('guardar.png', 'Guardar', 24, self.guardar_edicion)
        hbox.pack_start(boton, False, False, 0)
        vbox_fija.pack_start(frame, False, False, 0)
        self.model = gtk.ListStore(gtk.gdk.Pixbuf, str)
        self.imagenes = Widgets.TreeViewId('Imágenes', ('V.Previa', 'Archivo'))
        self.imagenes.set_liststore((gtk.gdk.Pixbuf, str))
        self.imagenes.escribir((
            [gtk.gdk.pixbuf_new_from_file_at_size('images/fondos/biblia.jpg', 50, 50), 'biblia.jpg'],
            [gtk.gdk.pixbuf_new_from_file_at_size('images/fondos/worship.jpg', 50, 50), 'worship.jpg'],
            ))
        #self.imagenes = gtk.FileChooserWidget()
        vbox_fija.pack_start(self.imagenes, False, False, 0)
        self.imagenes.scroll.set_size_request(200, 200)
        frame = Widgets.Frame('OSD')
        hbox = gtk.HBox(False, 0)
        self.entry_OSD = Widgets.Texto(64)
        self.entry_OSD.set_size_request(200, 25)
        hbox.pack_start(self.entry_OSD, True, True, 0)
        boton = Widgets.Button('mostrar.png', '', 24, self.mostrar_OSD)
        hbox.pack_start(boton, False, False, 0)
        frame.add(hbox)
        vbox_fija.pack_start(frame, False, False, 0)
        self.show_all()
        self.vista_previa.open(url)
        try:
            f = file('outs/escogidas.js', 'rb')
            escogidas = json.loads(f.read())
        except:
            self.http.escogidas = []
        else:
            print 'ESCOGIDAS'
            self.http.escogidas = escogidas
            self.seleccionados.escribir(escogidas)
            f.close()
        try:
            f = file('outs/repertorio.js', 'rb')
            repertorio = json.loads(f.read())
        except:
            self.http.repertorio = []
        else:
            print 'REPERTORIO'
            self.http.repertorio = repertorio
            self.repertorio.escribir(repertorio)
            f.close()
        self.repertorio.connect('activado', self.usar_cancion)
        self.seleccionados.connect('activado', self.mostrar_letras)
        self.parrafos.connect('activado', self.proyectar_letras)
        self.imagenes.connect('activado', self.cambiar_fondo)
        self.repertorio_id = None
        self.fullscreen = False
        self.biblia = Biblia()

    def login(self, *args):
        return
        self.vista_previa.open('http://%s/musica/login?session=%s&next=/musica/multimedia' % (self.http.dominio, self.http.sessionid))
        self.proyector.open('http://%s/musica/login?session=%s&next=/musica/multimedia' % (self.http.dominio, self.http.sessionid))

    def sincronizar(self, *args):
        datos = self.http.load('sincronizar', {'nada': 1})
        self.http.repertorio = datos['repertorio']
        self.http.escogidas = datos['escogidas']
        self.repertorio.escribir(self.http.repertorio)
        self.seleccionados.escribir(self.http.escogidas)
        self.backup_escogidas()
        f = file('outs/repertorio.js', 'wb')
        f.write(json.dumps(self.http.repertorio))
        f.close()

    def fullscreen(self, *args):
        if self.fullscreen:
            try:
                self.proyector.unfullscreen()
            except:
                url = 'http://%s/musica/login?session=%s&next=/musica/multimedia' % (self.http.dominio, self.http.sessionid)
                self.proyector = Chrome.Window(url)
                self.fullscreen = False
            else:
                self.fullscreen = False
        else:
            try:
                self.proyector.fullscreen()
            except:
                url = 'http://%s/musica/login?session=%s&next=/musica/multimedia' % (self.http.dominio, self.http.sessionid)
                self.proyector = Chrome.Window(url)
                self.fullscreen = False
            else:
                self.fullscreen = True

    def buscar_versiculo(self, *args):
        self.biblia.version(self.version.get_text())
        cita = self.entry_versiculo.get_text()
        texto = self.biblia.get(cita)
        self.text_mostrar.set_text(texto)
        self.enviar_proyector()

    def limpiar(self, *args):
        self.text_mostrar.set_text('')
        self.enviar_proyector()

    def mas_grande(self, *args):
        self.proyector.execute_script('masgrande();')

    def menos_grande(self, *args):
        self.proyector.execute_script('menosgrande();')

    def backup_escogidas(self):
        f = file('outs/escogidas.js', 'wb')
        f.write(json.dumps(self.http.escogidas))
        f.close()

    def usar_cancion(self, widget, fila):
        self.seleccionados.model.append(fila)
        self.http.escogidas.append(list(fila))
        self.backup_escogidas()

    def mostrar_letras(self, widget, fila):
        letras = fila[len(fila) - 2]
        i = 0
        data = []
        for p in letras.split('\r\n\r\n'):
            i += 1
            data.append((p, i))
        self.parrafos.escribir(data)
        self.repertorio_id = fila[len(fila) - 1]
        self.parrafo_id = None

    def cambiar_fondo(self, widget, fila):
        print fila[0], fila[1]
        self.vista_previa.execute_script('fondo("%s");' % fila[1])
        self.proyector.execute_script('fondo("%s");' % fila[1])

    def proyectar_letras(self, widget, fila):
        letras = fila[0]
        self.text_mostrar.set_text(letras)
        self.parrafo_id = fila[1]
        self.enviar_proyector()

    def enviar_proyector(self):
        letras = self.text_mostrar.get_text()
        letras = letras.replace('\r\n', '</br>')
        letras = letras.replace('\r', '</br>')
        letras = letras.replace('\n', '</br>')
        self.vista_previa.execute_script('escribir("%s")' % letras)
        self.proyector.execute_script('escribir("%s")' % letras)

    def anterior(self, *args):
        texto = self.biblia.anterior()
        self.text_mostrar.set_text(texto)
        self.enviar_proyector()

    def siguiente(self, *args):
        texto = self.biblia.siguiente()
        self.text_mostrar.set_text(texto)
        self.enviar_proyector()

    def mostrar_edicion(self, *args):
        self.enviar_proyector()

    def guardar_edicion(self, *args):
        if self.parrafo_id is None:
            return Widgets.Alerta('error.png', 'No ha seleccionado el párrafo a corregir.')
        texto = self.text_mostrar.get_text()
        self.parrafos.modificar('LETRAS', self.parrafo_id, texto)
        self.enviar_proyector()
        letras = ''
        for p in self.parrafos.model:
            letras += p[0] + '\r\n\r\n'
        self.seleccionados.modificar('*LETRAS', self.repertorio_id, letras)
        self.repertorio.modificar('*LETRAS', self.repertorio_id, letras)
        datos = {
            'letras': letras[0:-4],
            'repertorio_id': self.repertorio_id
        }
        self.backup_escogidas()
        self.http.load('guardar-letras', datos)

    def mostrar_versiculo(self, *args):
        pass
    def mostrar_OSD(self, *args):
        pass

    def ticketera(self, widgets, event):
        if event.button == 1:
            x = int(event.x)
            y = int(event.y)
            t = event.time
            self.menu.popup(None, None, None, event.button, t)
            self.menu.show_all()
            return True

    def impresora_serial(self, menu, puerto):
        self.http.ticketera.conectar_serial(puerto)

    def impresora_paralela(self, *args):
        self.http.ticketera.paralela()

    def impresora_probar(self, *args):
        self.http.ticketera.probar()

    def impresora_reimprimir(self, *args):
        self.http.ticketera.reimprimir()

    def cerrar(self, *args):
        self.destroy()

class Biblia:

    def __init__(self):
        global libros
        self.libros = libros
        for l in self.libros:
            l[3] = re.compile(l[1])
        self.version_nombre = None
        self.dict = {}
        self.libro = u'Génesis'
        self.capitulo = 1
        self.desde = 1
        self.hasta = 1

    def version(self, nombre):
        if self.version_nombre != nombre:
            archivo = file('biblias/' + nombre + '.json', 'rb')
            self.dict = json.loads(archivo.read())
            archivo.close()
            self.version_nombre = nombre
            print 'LIBROS', len(self.dict)
        else:
            pass

    def get_libro(self, abr):
        abr = abr.lower()
        for l in self.libros:
            if l[2] == abr:
                return l[0]
            elif l[3].search(abr):
                return l[0]
            else:
                print abr, l[1]

        return False


    def get(self, cita):
        n = cita.find(' ')
        if n:
            libro = self.get_libro(cita[:n])
            if libro:
                numeros = cita[n + 1:]
                m = numeros.find(':')
                if m < 0:
                    m = numeros.find('.')
                    if m < 0:
                        m = numeros.find(' ')
                        if m < 0:
                            return ''
                capitulo = numeros[:m]
                versiculos = numeros[m + 1:]
                p = versiculos.find('-')
                if p > 0:
                    desde = int(versiculos[:p])
                    hasta = int(versiculos[p + 1:])
                else:
                    desde = int(versiculos)
                    hasta = int(versiculos)
                self.libro = unicode(libro)
                self.capitulo = int(capitulo)
                self.desde = desde
                self.hasta = hasta
                return self.versiculo()
            return ''
        else:
            return ''

    def versiculo(self):
        capitulo = self.dict[self.libro][str(self.capitulo)]
        if self.desde != self.hasta:
            texto = '%s %s:%s-%s\n' % (self.libro, self.capitulo, self.desde, self.hasta)
        else:
            texto = '%s %s:%s\n' % (self.libro, self.capitulo, self.desde)
        i = self.desde - 1
        while i < self.hasta:
            try:
                texto += '%d %s\n' % (i + 1, capitulo[i])
            except:
                return texto + 'Fin del Libro'
            i += 1
        return texto

    def siguiente(self):
        self.desde = self.hasta + 1
        self.hasta = self.desde
        try:
            self.dict[self.libro][str(self.capitulo)][self.desde - 1]
        except:
            self.capitulo += 1
            self.desde = 1
            self.hasta = 1
            try:
                self.dict[self.libro][str(self.capitulo)][self.desde - 1]
            except:
                return 'Fin del libro'
        return self.versiculo()

def preparar_biblia(self):
    import urllib3
    version = 'RVR60'
    http = urllib3.HTTPConnectionPool('api.biblia.com')
    f = file(version + '.json', 'rb')
    biblia = json.loads(f.read())
    f.close()
    i = 0
    for l in libros:
        i += 1
        if unicode(l[0]) in biblia:
            print i, l[0], 'YA ESTA'
            continue
        print i, l[0], 'BUSCAR'
        l[3] = l[2].lower().replace(' ', '')
        cap = 1
        vers = 1
        respuesta = True
        fin_capitulo = False
        while respuesta:
            versiculo = (l[2] + '%d:%d' % ( cap, vers))
            url = '/v1/bible/content/'+version+'.txt.js?passage='+versiculo.replace(' ', '%20')+'&key=90aa8a24bcb98b1987b1865f61dd8cb6'
            respuesta = http.urlopen('GET', url)
            try:
                respuesta = json.loads(respuesta.data)
            except:
                if fin_capitulo:
                    respuesta = False
                else:
                    cap += 1
                    vers = 1
                    respuesta = True
                    fin_capitulo = True
            else:
                fin_capitulo = False
                data =  respuesta['text']
                if l[0] in biblia:
                    if cap in biblia[l[0]]:
                        biblia[l[0]][cap].append(data)
                        print l[0], cap, vers
                    else:
                        biblia[l[0]][cap] = [data]
                        print l[0], cap, vers
                else:
                    biblia[l[0]] = {cap: [data]}
                    print l[0], cap, vers
                vers += 1
        f = file(version + '.json', 'wb')
        f.write(json.dumps(biblia))
        f.close()

if __name__ == '__main__':
    #a = Biblia()
    #import Principal
    #a.http = Principal.Http(2)
    #Ventana(a, 0.1, 'Hoy')
    #gtk.main()
    preparar_biblia(1)
    biblia = Biblia()
    biblia.version('RVR60')
    for l in libros:
        if not l[0] in biblia.dict.keys():
            print l[0]
    print biblia.dict.keys()