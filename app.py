from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_file
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, DateField
from flask_wtf.file import FileField
from docxtpl import DocxTemplate
import array
from functools import wraps
from datetime import datetime


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("No tienes permisos", 'danger')
            return redirect(url_for('Login'))
    return wrap            

def si_no(var1, var2):
    if var1 == var2 :
        return "X"
    else :
        return " "

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def guarda_respuesta(var1):
    if not var1:
        return 'no'
    else:
        return var1[0]

def comprueba_input(var):
    if not var:
        return 'No Informa'
    else:
        return var

def descarga_archivo(filename):
    print("en la funcion")
    return send_file(filename, as_attachment=True, attachment_filename= filename)

app = Flask(__name__, template_folder='templates')
application = app
app.secret_key = "secret1234"

# Config MySQL
app.config['MYSQL_HOST'] = 'HOST'
app.config['MYSQL_USER'] = 'USER'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'DB'
app.config['MYSQL_PORT'] = port
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route('/index')
@is_logged_in
def index():
    return render_template('Home.html')
    
@app.route('/')
def inicio():
    return redirect(url_for('Login'))

class Formulario(Form):
    nombre = StringField('Nombre Completo', [validators.Length(min=0, max = 100)])
    rut = StringField('RUT',[validators.DataRequired(message='Campo Requerido')])
    fecha_aplicacion = StringField('Fecha de Aplicación', [validators.Length(min=0,max=10)])
    fecha_nacimiento = StringField('Fecha de Nacimiento: dd/mm/yy', [validators.Length(min=0,max=10)])
    nacionalidad = StringField('Nacionalidad', [validators.Length(min=0,max=18)])
    email = StringField('Email', [validators.Length(min=0,max=100), validators.DataRequired()])
    derivacion_empresa = StringField('Derivado Entrevista Laboral (Empresa)', [validators.Length(min=0,max=50)])
    curso_cap = StringField('Curso de capacitación', [validators.Length(min=0,max=50)])
    nivelacion_estudio = StringField('Nivelación de Estudio', [validators.Length(min=0,max=50)])
    apoyo_soclab = StringField('Apoyo Social – Laboral', [validators.Length(min=0,max=50)])
    der_coloc = StringField('Derivado a Vacante Laboral', [validators.Length(min=0,max=50)])
    evycertif_comp = StringField('Evaluación y Certificación de competencia laboral', [validators.Length(min=0,max=50)])
    emprendimiento = StringField('Emprendimiento', [validators.Length(min=0,max=50)])
    apoyosocialxtra = StringField('Apoyo Social Extra Omil', [validators.Length(min=0,max=50)])
    der_orientador = StringField('Derivado a Profesional Orientador', [validators.Length(min=0,max=50)])
    seguro_cesantia = StringField('Seguro de Cesantia', [validators.Length(min=0,max=50)])
    mot_derivacion = StringField('Motivo de Derivación', [validators.Length(min=0,max=50)])
    sintat_inicial = StringField('Síntesis de Atención Inicial', [validators.Length(min=0,max=20)])
    tel_not = StringField('Teléfono de Notificaciones', [validators.Length(min=0,max=10)])
    tel_alt = StringField('Teléfono Alternativo', [validators.Length(min=0,max=10)])
    experiencia = StringField('Experiencia', [validators.Length(min=0,max=100)])
    nivel_estudios = StringField('Nivel Educacional', [validators.Length(min=0,max=100)])
    bne = StringField('Bolsa Nacional de Empleo', [validators.Length(min=0,max=50)])
    plat_municipal = StringField('Síntesis de Atención Inicial', [validators.Length(min=0,max=50)])
    otro = StringField('Otro', [validators.Length(min=0,max=50)])
    profesion = StringField('Profesión', [validators.Length(min=0,max=50)])
    trabajos_previos = StringField('Trabajos Previos', [validators.Length(min=0,max=100)])
    direccion = StringField('Dirección', [validators.Length(min=0,max=150)])
    comuna = StringField('Comuna', [validators.Length(min=0,max=20)])
    discapacidad = StringField('Discapacidad', [validators.Length(min=0,max=20)])
    preferencias = StringField('Áreas de Interés', [validators.Length(min=0,max=100)])
    certificados = StringField('Certificados')
    tipo_licencia_especial = StringField('Tipo de Licencia')
    diplomas_certificados_form = FileField('Adjuntar Diploma de Certificación')
    licencias_especiales_form = FileField('Adjuntar Licencia Especial')
    subsidios = StringField('Subsidios (SEJ - BTM)')

class Funcionario(Form):
    #solamente una prueba, hay que agregar el resto de los parametros 
    nombre_funcionario = StringField('Nombre del Funcionario', [validators.Length(min = 4, max = 50)])
    contraseña = PasswordField('Contraseña', [validators.DataRequired()
    ])     

class Formulario_oferta_laboral(Form):
    #Datos de la empresa
    fecha_solicitud = StringField('Fecha de solicitud', [validators.Length(min=0, max=25)])
    nombre_empresa = StringField('Nombre de la Empresa o PYME', [validators.Length(min=0, max=25)])
    rut = StringField('Rut de la Empresa o PYME', [validators.Length(min=0, max=25)])
    direccion_comercial = StringField('Dirección Comercial', [validators.Length(min=0, max=25)])
    nombre_solicitante = StringField('Nombre Solicitante', [validators.Length(min=0, max=25)])
    telefono_1 = StringField('Teléfono de Contacto 1', [validators.Length(min=0, max=25)])
    correo_solicitante = StringField('Correo Solicitante', [validators.Length(min=0, max=25)])
    #Descripcion de la oferta
    descripcion_oferta = StringField('Descripción de la Oferta', [validators.Length(min=0, max=25)])
    #Perfil Laboral
    habilidades_requeridas = StringField('Habilidades necesarias para desempeñar el cargo', [validators.Length(min=0, max=25)])
    rango_de_edad = StringField('Rango de Edad', [validators.Length(min=0, max=25)])
    nivel_estudios_requerido = StringField('Nivel de Estudios', [validators.Length(min=0, max=25)])
    horario_de_trabajo = StringField('Horario de Trabajo', [validators.Length(min=0, max=25)])
    sueldo = StringField('Sueldo', [validators.Length(min=0, max=25)])
    años_experiencia = StringField('Años de Experiencia', [validators.Length(min=0, max=25)])
    numero_vacantes = StringField('Número de Vacantes', [validators.Length(min=0, max=25)])
    tipo_contrato = StringField('Tipo de Contrato', [validators.Length(min=0, max=25)])
    lugar_de_trabajo = StringField('Lugar de Trabajo', [validators.Length(min=0, max=25)])
    sexo = StringField('Sexo', [validators.Length(min=0, max=25)])
    fecha_entrevista = StringField('Fecha de la Entrevista', [validators.Length(min=0, max=25)])
    hora_entrevista = StringField('Hora de la Entrevista', [validators.Length(min=0, max=25)])
    lugar_entrevista = StringField('Lugar de la Entrevista', [validators.Length(min=0, max=25)])
    info_entrevista = DateTimeField('Fecha y Hora de la Entrevista')
    #Documentos solicitados para entrevista 
    curriculum = StringField('Curriculum', [validators.Length(min=0, max=25)])
    copia_CI = StringField('Copia Cédula de Identidad', [validators.Length(min=0, max=25)])
    certificado_antecedentes = StringField('Certificado de Antecedentes', [validators.Length(min=0, max=25)])
    certificado_estudios = StringField('Certificado de Estudios', [validators.Length(min=0, max=25)])
    licencia_conducir = StringField('Licencia de Conducir', [validators.Length(min=0, max=25)])
    hoja_vida_conductor = StringField('Hoja de Vida del Conductor', [validators.Length(min=0, max=25)])
    ultimo_finiquito = StringField('Último Finiquito', [validators.Length(min=0, max=25)])
    licencia_militar = StringField('Licencia Militar', [validators.Length(min=0, max=25)])
    recomendaciones = StringField('Recomendaciones', [validators.Length(min=0, max=25)])
    #Politicas inclusivas y de inserción laboral
    extranjeros_visa_temp = StringField('Extranjeros con Visa Temporaria', [validators.Length(min=0, max=25)])
    personas_ant_penales = StringField('Personas con Antecedentes Penales', [validators.Length(min=0, max=25)])
    personas_cap_dif = StringField('Personas con Capacidades Diferentes', [validators.Length(min=0, max=25)])
    #Observaciones 
    observaciones = StringField('Observaciones', [validators.Length(min=0, max=25)])

class busqueda_usuarios(Form):
    busqueda = StringField('Parámetro de búsqueda')
    caracteristica = StringField('Característica buscada')
    rut_busqueda = StringField('Rut')
    caracteristica_comuna = StringField('Caracteristica Comuna')
    caracteristica_nacionalidad =  StringField('Caracteristica Nacionalidad')
    caracteristica_profesion =  StringField('Caracteristica Profesión')
    caracteristica_area_interes =  StringField('Caracteristica Área de Interés')
    caracteristica_nivel_estudios =  StringField('Caracteristica Nivel de Estudios')
    caracteristica_tecnico_profesional =  StringField('Caracteristica Técnico Profesional')
    caracteristica_discapacidad =  StringField('Caracteristica Discapacidad')


@app.route('/register', methods =['GET','POST'])
@is_logged_in
def registro():
    form = Formulario(request.form)
    if request.method == 'POST' and form.validate():
        nombre = comprueba_input(form.nombre.data)
        rut    = comprueba_input(form.rut.data) 
    
        if request.form['fecha_aplicacion'] == '':
            fecha_aplicacion = datetime.today()
        else:
            fecha_aplicacion = datetime.strptime(request.form['fecha_aplicacion'], '%Y-%m-%d')
        
        if request.form['fecha_nacimiento'] == '':
            fecha_nacimiento = 'No Informa'
        else:
            fecha_nacimiento =  datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d')

        nacionalidad     = form.nacionalidad.data
        email = comprueba_input(form.email.data) 

        derivacion_empresa_list = request.form.getlist('derivacion_empresa')
        derivacion_empresa = guarda_respuesta(derivacion_empresa_list)

        curso_cap_list = request.form.getlist('curso_cap')
        curso_cap = guarda_respuesta(curso_cap_list) 

        nivelacion_estudio_list = request.form.getlist('nivelacion_estudio')
        nivelacion_estudio = guarda_respuesta(nivelacion_estudio_list) 

        apoyo_soclab_list = request.form.getlist('apoyo_soclab')
        apoyo_soclab = guarda_respuesta(apoyo_soclab_list) 

        subsidios_list = request.form.getlist('subsidios')
        subsidios = guarda_respuesta(subsidios_list)

        der_coloc_list = request.form.getlist('der_coloc') 
        der_coloc = guarda_respuesta(der_coloc_list)

        evycertif_comp_list = request.form.getlist('evycertif_comp')
        evycertif_comp = guarda_respuesta(evycertif_comp_list)

        emprendimiento_list = request.form.getlist('emprendimiento')
        emprendimiento = guarda_respuesta(emprendimiento_list)  

        apoyosocialxtra_list = request.form.getlist('apoyosocialxtra')
        apoyosocialxtra = guarda_respuesta(apoyosocialxtra_list)  

        der_orientador_list = request.form.getlist('der_orientador')
        der_orientador = guarda_respuesta(der_orientador_list)  

        seguro_cesantia_list = request.form.getlist('seguro_cesantia')
        seguro_cesantia = guarda_respuesta(seguro_cesantia_list)  

        mot_derivacion = comprueba_input(form.mot_derivacion.data) 
        sintat_inicial = comprueba_input(form.sintat_inicial.data) 
        tel_not = comprueba_input(form.tel_not.data) 
        tel_alt = comprueba_input(form.tel_alt.data) 

        area_interes_list = request.form.get('area-interes')
        area_interes = area_interes_list

        nivel_estudios_list = request.form.getlist('nivel_estudios')
        nivel_estudios = guarda_respuesta(nivel_estudios_list)  

        bne_list = request.form.getlist('bne')
        bne = guarda_respuesta(bne_list)  

        plat_municipal_list = request.form.getlist('plat_municipal')
        plat_municipal = guarda_respuesta(plat_municipal_list)  

        otro = comprueba_input(form.otro.data) 
        profesion = comprueba_input(form.profesion.data) 
        trabajos_previos = comprueba_input(form.trabajos_previos.data) 
        direccion = comprueba_input(form.direccion.data)
        comuna = comprueba_input(form.comuna.data) 

        discapacidad = comprueba_input(request.form.get('discapacidad')) 
        if discapacidad == 'Si':
            discapacidad_si = 'X'
            discapacidad_no = ' '
        else:
            discapacidad_si = ' '
            discapacidad_no = 'X'            

        experiencia = comprueba_input(form.experiencia.data) 

        tecnico_profesional_list = request.form.getlist('tecnico-profesional')
        tecnico_profesional = guarda_respuesta(tecnico_profesional_list) 

        sector_tc = comprueba_input(request.form.get("sector-tc")) 

        tiene_certificados_list = request.form.getlist('certificado')
        tiene_certificados = guarda_respuesta(tiene_certificados_list) 

        numero_certificados = comprueba_input(request.form.get("numero-certificados")) 

        lugar_certificados = comprueba_input(request.form.get("certificado-donde")) 

        duracion_certificacion = comprueba_input(request.form.get("duracion-certificados")) 

        duracion_curso_certificacion = comprueba_input(request.form.get("duracion-certificacion")) 

        #diplomas_certificados_nb = request.files['diploma-certificado']
        diplomas_certificados = " "
       
        tiene_licencias_especiales = comprueba_input(request.form.get("licencia-especial")) 
        tipo_de_licencia_especial = comprueba_input(form.tipo_licencia_especial.data) 

        licencia_especial_lugar = comprueba_input(request.form.get("licencia-especial-donde")) 

        duracion_licencia_especial = comprueba_input(request.form.get("duracion-licencia-especial")) 

        #licencia_doc_nb = request.files['diploma-licencia']
        licencia_doc = " "

        cur = mysql.connection.cursor()

        resultado = cur.execute("SELECT * FROM usuario WHERE rut= %s", [rut])
        print(resultado)
        if resultado > 0:
            flash('Usuario ya está registrado en el sistema, para ver su información vaya a perfil de usuario', 'danger')
            cur.close()
            return redirect(url_for('registro'))
        else:
            cur.close()

            cur = mysql.connection.cursor()
            
            cur.execute("INSERT INTO usuario(nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, area_interes, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad_si, experiencia, tecnico_profesional, sector_tc, tiene_certificados, numero_certificados, lugar_certificados, duracion_certificacion, duracion_curso_certificacion, diplomas_certificados, tiene_licencias_especiales, tipo_de_licencia_especial, licencia_especial_lugar, duracion_licencia_especial, licencia_doc, subsidios,discapacidad_no) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, area_interes, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad_si, experiencia, tecnico_profesional, sector_tc, tiene_certificados, numero_certificados, lugar_certificados, duracion_certificacion, duracion_curso_certificacion, diplomas_certificados, tiene_licencias_especiales, tipo_de_licencia_especial, licencia_especial_lugar, duracion_licencia_especial, licencia_doc, subsidios, discapacidad_no])

            mysql.connection.commit()

            cur.close()

            cur = mysql.connection.cursor()
            resultado = cur.execute("SELECT * FROM usuario WHERE rut= %s", [rut])
            #print('el resultado')
            #print(resultado)
            try:
                if resultado > 0:
                    data = cur.fetchone()
                print(data)
                test = DocxTemplate('template_anexo1.5.docx')
                filename =  data['nombre'] + "anexo1.docx"
                test.render(data)
                test.save(filename)
                flash("El usuario fue registrado correctamente", 'success' )
                #return send_file(filename, as_attachment=True, attachment_filename= nombre + '_anexo1.docx'), render_template('register.html', form = form)
                return redirect(url_for('descargar_archivo', filename = filename))
            except:
                flash("Ocurrió un error inesperado, por favor revise los campos e inténtelo nuevamente", 'danger')
                return render_template('register.html', form=form)
    return render_template('register.html', form=form)    

@app.route('/descarga/<filename>')
@is_logged_in
def descargar_archivo(filename):
    return send_file(filename, as_attachment=True, attachment_filename= filename)


@app.route('/perfil', methods=['GET', 'POST'])
@is_logged_in
def ver_perfil():
    form = busqueda_usuarios(request.form)
    if request.method == 'POST':
        if request.form['button'] == 'Buscar Usuario':
            RUT = form.rut_busqueda.data
            cur = mysql.connection.cursor()
            buscado = cur.execute("SELECT * FROM usuario WHERE rut= %s", [RUT])
                
            if buscado <= 0:
                flash('Usuario no encontrado', 'danger')
                return render_template('perfil.html', form=form)      

            if buscado > 0:
                data = cur.fetchone()

            cur.close()
            #flash('usuario encontrado', 'success')
            #return redirect(url_for('vista_perfil', datos = data))
            return render_template('perfil_de_usuario.html', usuario = data)

        elif request.form['button'] == 'Buscar Usuarios':
            parametro = form.busqueda.data
            print(parametro)
            if parametro == 'placeholder':
                return render_template('perfil.html', form = form)

            cursor = mysql.connection.cursor()

            if parametro == 'comuna':                                           #query comuna
                caracteristica = form.caracteristica_comuna.data
                print(caracteristica)
                query = "SELECT * FROM usuario WHERE comuna = %s;"
                buscado = "COMUNA"
            elif parametro == 'nacionalidad':                                   #query nacionalidad 
                caracteristica = form.caracteristica_nacionalidad.data
                print(caracteristica)
                query = "SELECT * FROM usuario WHERE nacionalidad = %s;"
                buscado = "NACIONALIDAD"
            elif parametro == 'profesion':                                      #query profesion
                palabra_buscada = form.caracteristica_profesion.data
                caracteristica = "%" + palabra_buscada + "%"
                print(caracteristica)
                query = "SELECT * FROM usuario WHERE profesion LIKE %s;"
                buscado = "PROFESIÓN"
            elif parametro == 'area_interes':                                   #query area de interés
                caracteristica = form.caracteristica_area_interes.data
                print(caracteristica)
                query = "SELECT * FROM usuario WHERE area_interes = %s;"
                buscado = "ÁREA DE INTERÉS"
            elif parametro == 'nivel_estudios':                                 #query nivel de estudios
                caracteristica = form.caracteristica_nivel_estudios.data
                print(caracteristica)
                query = "SELECT * FROM usuario WHERE nivel_estudios = %s;"
                buscado = "NIVEL DE ESTUDIOS"
            elif parametro == 'tecnico_profesional':                            #query tecnico profesional
                caracteristica = guarda_respuesta(request.form.getlist('caracteristica_tecnico_profesional')) 
                print(caracteristica)
                query = "SELECT * FROM usuario WHERE tecnico_profesional = %s;"
                buscado = "TÉCNICO PROFESIONAL"
            elif parametro == 'discapacidad':                                   #query discapcidad

                caracteristica = guarda_respuesta(request.form.getlist('caracteristica_discapacidad')) 
                print(caracteristica)
                if caracteristica == 'Si':
                    query = "SELECT * FROM usuario WHERE discapacidad_si = %s;"
                elif caracteristica == 'No':
                    query = "SELECT * FROM usuario WHERE discapacidad_no = %s;"
                aux = caracteristica
                caracteristica = "X"
                buscado = "DISCAPACIDAD"

            cursor.execute(query,  (caracteristica,) )
            print(query, caracteristica)
            
            resultado_busqueda = cursor.fetchall()
            i = 0
            for data in resultado_busqueda:
                print(i, data['nombre'])
                i = i + 1

           # if query <= 0:
            #    flash('Hubo un problema con la query', 'danger')
             #   print("hubo un problema con la query")
              #  print(resultado_busqueda)
               # return render_template('perfil.html')

            cuenta = cursor.rowcount
            if buscado == 'DISCAPACIDAD':
                caracteristica = aux
            cursor.close()
            
            return render_template('lista.html', 
                                    form = form,
                                    parametro = parametro,
                                    caracteristica = caracteristica,
                                    datos = resultado_busqueda, 
                                    buscado = buscado,
                                    cuenta = cuenta
            )
    #flash('Página de búsqueda de perfil de usuario')
    return render_template('perfil.html', form=form) 

#@app.route('/perfil_usuario/<datos>', methods=['GET', 'POST'])
#@is_logged_in
#def vista_perfil(datos):
#    render_template('perfil_de_usuario.html', usuario = datos)

@app.route('/Anexos', methods =['GET','POST'])
@is_logged_in
def Template():
    form = Formulario(request.form)
    if request.method == 'POST':
        RUT = form.rut.data
        test = DocxTemplate('template_anexo1.5.docx')
 
        cur = mysql.connection.cursor()
        
        resultado = cur.execute("SELECT * FROM usuario WHERE rut= %s", [RUT])

        if resultado <= 0:
            flash('Usuario no encontrado', 'danger')
            return render_template('Anexos.html', form=form)      

        if resultado > 0:
            data = cur.fetchone()
            flash('Usuario encontrado', 'success')
            
            
        #flash( 'Rut = ' + data['rut'])
        filename =  data['rut'] + ".docx"
        test.render(data)
        test.save(filename)
        
        cur.close()
        flash('Anexo creado y descargado correctamente', 'success')
        
        return send_file(filename, as_attachment=True, attachment_filename= RUT + '_anexo1.docx')

    return render_template('Anexos.html', form=form)      

@app.route('/Registro', methods = ['GET', 'POST'])
def Login():
    form = Funcionario(request.form)
    if request.method == 'POST':
        nombre_usuario = form.nombre_funcionario.data
        contraseña = form.contraseña.data

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM funcionario WHERE nombre = %s", [nombre_usuario]) 

        if result > 0:
            data = cur.fetchone()
            password = data['contraseña']
            if contraseña == password:
                session['logged_in'] = True
                session['username'] = nombre_usuario

                flash('conectado correctamente', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Contraseña o usuario no existen'
                return render_template('Login.html', error = error)    
            cur.close()
        else:
            error = 'Usuario no existe'
            return render_template('Login.html', error = error)    

    return render_template('Login.html', form = form)    

@app.route('/Ingresar-oferta', methods=['GET', 'POST'])
@is_logged_in
def nueva_oferta_laboral():
    form = Formulario_oferta_laboral(request.form)
    if request.method == 'POST' and form.validate():
        #Datos Empresa
        nombre_empresa = form.nombre_empresa.data
        rut_empresa = form.rut.data
        direccion_comercial = form.direccion_comercial.data
        nombre_solicitante = form.nombre_solicitante.data
        telefono_empresa = form.telefono_1.data
        correo_solicitante = form.correo_solicitante.data
        fecha_solicitud = datetime.strptime(request.form['fecha_solicitud'], '%Y-%m-%d')

        #Perfil Laboral y Dscripción de la Empresa
        habilidades_requeridas = form.habilidades_requeridas.data
        rango_de_edad = form.rango_de_edad.data
        nivel_estudios_requerido = form.nivel_estudios_requerido.data
        horario_de_trabajo = form.horario_de_trabajo.data
        sueldo = form.sueldo.data
        años_experiencia = form.años_experiencia.data
        numero_vacantes = form.numero_vacantes.data
        tipo_contrato = form.tipo_contrato.data
        lugar_de_trabajo = form.lugar_de_trabajo.data
        sexo = form.sexo.data
        fecha_entrevista = form.fecha_entrevista.data
        hora_entrevista = form.hora_entrevista.data
        lugar_entrevista = form.lugar_entrevista.data
        #info_entrevista = form.info_entrevista.data

        #Documentos Solicitados para la entrevista
        curriculum = request.form.get('curriculum')
        copia_CI = request.form.get('copia_CI')
        certificado_antecedentes = request.form.get('certificado_antecedentes')
        certificado_estudios = request.form.get('certificado_estudios')
        licencia_conducir = request.form.get('licencia_conducir')
        hoja_vida_conductor = request.form.get('hoja_vida_conductor')
        ultimo_finiquito = request.form.get('ultimo_finiquito')
        licencia_militar = request.form.get('licencia_militar')
        recomendaciones = form.recomendaciones.data

        #Polìticas inclusivas y de inserciòn social
        extranjeros_visa_temp = request.form.get('extranjeros_visa_temp')
        personas_ant_penales = request.form.get('personas_ant_penales')
        personas_cap_dif = request.form.get('personas_cap_dif')

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO empresa(rut, nombre, direccion, telefono, representante) VALUES(%s,%s,%s,%s,%s)',[rut_empresa, nombre_empresa, direccion_comercial, telefono_empresa, nombre_solicitante])
        mysql.connection.commit()    
        cur.close()

        cur2 = mysql.connection.cursor()
        cur2.execute('INSERT INTO oferta_laboral(rut_empresa, nombre_empresa, fecha_solicitud, nombre_representante, telefono, habilidades_necesarias, rango_edad, nivel_estudios, horario_trabajo, sueldo, años_de_experiencia, numero_vacantes, tipo_contrato, lugar_trabajo, sexo ,fecha_entrevista ,hora_entrevista, lugar_entrevista, curriculum, copia_ci, certificado_antecedentes, certificado_estudios, licencia_conducir, hoja_vida_conductor, ultimo_finiquito, licencia_militar, recomendaciones, extranjeros_visa_temp, personas_antecedentes_penales, personas_capacidades_diferentes) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[rut_empresa, nombre_empresa, fecha_solicitud, nombre_solicitante, telefono_empresa, habilidades_requeridas, rango_de_edad, nivel_estudios_requerido, horario_de_trabajo, sueldo, años_experiencia, numero_vacantes, tipo_contrato, lugar_de_trabajo, sexo, fecha_entrevista, hora_entrevista, lugar_entrevista, curriculum, copia_CI, certificado_antecedentes, certificado_estudios, licencia_conducir, hoja_vida_conductor, ultimo_finiquito, licencia_militar, recomendaciones, extranjeros_visa_temp, personas_ant_penales, personas_cap_dif])
        mysql.connection.commit()    
        cur2.close()


        flash('oferta ingresada correctamente', 'success')
        return redirect(url_for('nueva_oferta_laboral'))
        
    return render_template('ingresar_oferta.html', form = form)

if __name__ == '__main__':
    app.run(debug = True) #este debug se tiene que borrar para la fase final solo sirve para poder recargar el sevidor

@app.route('/info_general')
@is_logged_in
def line(): 

    etiquetas = ["SELECT COUNT(rut), comuna FROM usuario GROUP BY comuna ORDER BY COUNT(rut) DESC;", "SELECT COUNT(rut), nacionalidad FROM usuario GROUP BY nacionalidad ORDER BY COUNT(rut) DESC;"]

    info = []
    labels = [[],[]]
    values = [[],[]]
    max = 0
    for etiqueta in etiquetas:
        mycursor = mysql.connection.cursor()
        query = mycursor.execute(etiqueta)
        myresult = mycursor.fetchall()
        info.append(myresult)

    buscadores = ['comuna','nacionalidad']
    if query <= 0:
            flash('Hubo un problema con la query', 'danger')
            return render_template('info_general.html')

    elif query > 0:
        i = 0
        for data in info:
            for datos in data:
                print(" ")
                print(datos[buscadores[i]])
                labels[i].append(datos[buscadores[i]])
                values[i].append(datos['COUNT(rut)'])
                if datos['COUNT(rut)'] > max:
                    max = datos['COUNT(rut)']
            i = i + 1

    #copia_valores = values.copy()
    #copia_valores.sort()
    #max = copia_valores[0]
    print(labels)
    print(values)
    line_labels=labels
    line_values=values
    return render_template('info_general.html', title='Información General', max=max, labels=line_labels[0], values=line_values[0],
    labels2 = line_labels[1], values2 = line_values[1] )
