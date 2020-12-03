from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_file
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, DateField
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

app = Flask(__name__, template_folder='templates')
application = app
app.secret_key = "secret1234"

# Config MySQL
app.config['MYSQL_HOST'] = 'HOST'
app.config['MYSQL_USER'] = 'USER'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'DB'
app.config['MYSQL_PORT'] = 0000
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
    rut = StringField('RUT',[validators.Length(min=6, max = 12)])
    fecha_aplicacion = StringField('Fecha de Aplicación', [validators.Length(min=0,max=10)])
    fecha_nacimiento = StringField('Fecha de Nacimiento: dd/mm/yy', [validators.Length(min=0,max=10)])
    nacionalidad = StringField('Nacionalidad', [validators.Length(min=4,max=18)])
    email = StringField('Email', [validators.Length(min=0,max=35)])
    derivacion_empresa = StringField('Derivado Entrevista Laboral (Empresa)', [validators.Length(min=0,max=50)])
    curso_cap = StringField('Curso de capacitación', [validators.Length(min=0,max=50)])
    nivelacion_estudio = StringField('Nivelación de Estudio', [validators.Length(min=0,max=50)])
    apoyo_soclab = StringField('Apoyo Social – Laboral', [validators.Length(min=0,max=50)])
    der_coloc = StringField('Derivado a Colocación Laboral', [validators.Length(min=0,max=50)])
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
    nivel_estudios = StringField('Nivel de Estudios', [validators.Length(min=0,max=100)])
    bne = StringField('Bolsa Nacional de Empleo', [validators.Length(min=0,max=50)])
    plat_municipal = StringField('Síntesis de Atención Inicial', [validators.Length(min=0,max=50)])
    otro = StringField('Otro', [validators.Length(min=0,max=50)])
    profesion = StringField('Profesión', [validators.Length(min=0,max=50)])
    trabajos_previos = StringField('Trabajos Previos', [validators.Length(min=0,max=100)])
    direccion = StringField('Dirección', [validators.Length(min=0,max=20)])
    comuna = StringField('Comuna', [validators.Length(min=0,max=20)])
    discapacidad = StringField('Discapacidad', [validators.Length(min=0,max=20)])
    preferencias = StringField('Preferencias', [validators.Length(min=0,max=100)])

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
    telefono_2 = StringField('Teléfono de Contacto 2', [validators.Length(min=0, max=25)])
    telefono_3 = StringField('Teléfono de Contacto 3', [validators.Length(min=0, max=25)])
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


@app.route('/register', methods =['GET','POST'])
@is_logged_in
def registro():
    form = Formulario(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        rut    = form.rut.data
        
        fecha_aplicacion = datetime.strptime(request.form['fecha_aplicacion'], '%Y-%m-%d')
        fecha_nacimiento =  datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d')

        nacionalidad     = form.nacionalidad.data
        email = form.email.data

        derivacion_empresa_list = request.form.getlist('derivacion_empresa')
        derivacion_empresa = derivacion_empresa_list[0]

        curso_cap_list = request.form.getlist('curso_cap')
        curso_cap = curso_cap_list[0]

        nivelacion_estudio_list = request.form.getlist('nivelacion_estudio')
        nivelacion_estudio = nivelacion_estudio_list[0]

        apoyo_soclab_list = request.form.getlist('apoyo_soclab')
        apoyo_soclab = apoyo_soclab_list[0]

        der_coloc_list = request.form.getlist('der_coloc') 
        der_coloc = der_coloc_list[0]

        evycertif_comp_list = request.form.getlist('evycertif_comp')
        evycertif_comp = evycertif_comp_list[0]

        emprendimiento_list = request.form.getlist('emprendimiento')
        emprendimiento = emprendimiento_list[0]

        apoyosocialxtra_list = request.form.getlist('apoyosocialxtra')
        apoyosocialxtra = apoyosocialxtra_list[0]

        der_orientador_list = request.form.getlist('der_orientador')
        der_orientador = der_orientador_list[0]

        seguro_cesantia_list = request.form.getlist('seguro_cesantia')
        seguro_cesantia = seguro_cesantia_list[0]

        mot_derivacion = form.mot_derivacion.data
        sintat_inicial = form.sintat_inicial.data
        tel_not = form.tel_not.data
        tel_alt = form.tel_alt.data

        experiencia_list = request.form.getlist('experiencia')
        experiencia = experiencia_list[0]
        if experiencia_list[1]:
            experiencia = experiencia_list[0] + ',' + experiencia_list[1]

        nivel_estudios_list = request.form.getlist('nivel_estudios')
        nivel_estudios = nivel_estudios_list[0]

        bne_list = request.form.getlist('bne')
        bne = bne_list[0]

        plat_municipal_list = request.form.getlist('plat_municipal')
        plat_municipal = plat_municipal_list[0]

        otro = form.otro.data
        profesion = form.profesion.data
        trabajos_previos = form.trabajos_previos.data
        direccion = form.direccion.data
        comuna = form.comuna.data

        discapacidad_list = request.form.getlist('discapacidad')
        disc_si = si_no(discapacidad_list[0],'si')
        disc_no = si_no(discapacidad_list[0],'no')

        if disc_si == 'X':
            discapacidad = disc_si
        else:
            discapacidad = disc_no

        preferencias = form.preferencias.data


        cur = mysql.connection.cursor()
        
        #sql = "INSERT INTO usuario(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        #values = [nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, experiencia, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad, preferencias]

        #cur.execute(sql, values)

        cur.execute("INSERT INTO usuario(nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, experiencia, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad, preferencias) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, experiencia, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad, preferencias])

        mysql.connection.commit()

        cur.close()

        flash("Ingresado correctamente", 'success' )
        
        return redirect(url_for('registro'))

    return render_template('register.html', form=form)    

@app.route('/perfil', methods=['GET', 'POST'])
@is_logged_in
def ver_perfil():
    form = Formulario(request.form)
    if request.method == 'POST':
        RUT = form.rut.data
 
        cur = mysql.connection.cursor()
        
        buscado = cur.execute("SELECT * FROM usuario WHERE rut= %s", [RUT])
              
        if buscado <= 0:
            flash('Usuario no encontrado', 'danger')
            return render_template('perfil.html', form=form)      

        if buscado > 0:
            data = cur.fetchone()

        cur.close()
        #flash('usuario encontrado', 'success')


        return render_template('perfil_de_usuario.html', usuario=data)

    #flash('Página de búsqueda de perfil de usuario')
    return render_template('perfil.html', form=form) 

@app.route('/Anexos', methods =['GET','POST'])
@is_logged_in
def Template():
    form = Formulario(request.form)
    if request.method == 'POST':
        RUT = form.rut.data
        test = DocxTemplate('template_anexo1.5.docx')
 
        cur = mysql.connection.cursor()
        
        resultado = cur.execute("SELECT * FROM usuario WHERE rut= %s", [RUT])

        if resultado > 0:
            data= cur.fetchone()
            
            
        flash( 'Rut = ' + data['rut'])
        filename =  data['rut'] + ".docx"
        test.render(data)
        test.save(filename)
        
        cur.close()

        
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
def nueva_oferta_laboral():
    form = Formulario_oferta_laboral(request.form)
    if request.method == 'POST' and form.validate():

        nombre = form.nombre_empresa.data
        print(nombre)

        flash('nombre ingresado fue' + nombre)
        return render_template('ingresar_oferta.html', form = form)
    return render_template('ingresar_oferta.html', form = form)


if __name__ == '__main__':
    app.run(debug = True) #este debug se tiene que borrar para la fase final solo sirve para poder recargar el sevidor

