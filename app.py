from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_file
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from filler import Filler
from docxtpl import DocxTemplate
from mailmerge import MailMerge
import array
from functools import wraps




def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("no tienes permisos", 'danger')
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
app.config['MYSQL_HOST'] = 'sm9j2j5q6c8bpgyq.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'ukg47wvunvh3d7eu'
app.config['MYSQL_PASSWORD'] = 'iu55qaryfhglxqni'
app.config['MYSQL_DB'] = 'fcqf03dhrhk903lo'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route('/index')
@is_logged_in
def index():
    return render_template('home.html')
    

@app.route('/')
def inicio():
    return redirect(url_for('Login'))


class Formulario(Form):
    nombre = StringField('Nombre Completo', [validators.Length(min=0, max = 100)])
    rut = StringField('RUT',[validators.Length(min=6, max = 12)])
    fecha_aplicacion = StringField('Fecha de Aplicación', [validators.Length(min=0,max=10)])
    fecha_nacimiento = StringField('Fecha de Nacimiento: dd/mm/yy', [validators.Length(min=0,max=10)])
    nacionalidad = StringField('Nacionalidad', [validators.Length(min=4,max=18)])
    email = StringField('Email', [validators.Length(min=0,max=20)])
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
    contraseña = PasswordField('contraseña', [
        validators.DataRequired()
    ])     
    


@app.route('/register', methods =['GET','POST'])
@is_logged_in
def registro():
    form = Formulario(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        rut    = form.rut.data
        fecha_aplicacion = form.fecha_aplicacion.data
        fecha_nacimiento = form.fecha_nacimiento.data
        nacionalidad     = form.nacionalidad.data
        email = form.email.data
        derivacion_empresa = form.derivacion_empresa.data
        curso_cap = form.curso_cap.data
        nivelacion_estudio = form.nivelacion_estudio.data
        apoyo_soclab = form.apoyo_soclab.data
        der_coloc = form.der_coloc.data
        evycertif_comp = form.evycertif_comp.data
        emprendimiento = form.emprendimiento.data
        apoyosocialxtra = form.apoyosocialxtra.data
        der_orientador = form.der_orientador.data
        seguro_cesantia = form.seguro_cesantia.data
        mot_derivacion = form.mot_derivacion.data
        sintat_inicial = form.sintat_inicial.data
        tel_not = form.tel_not.data
        tel_alt = form.tel_alt.data
        experiencia = form.experiencia.data
        nivel_estudios = form.nivel_estudios.data
        bne = form.bne.data
        plat_municipal = form.plat_municipal.data
        otro = form.otro.data
        profesion = form.profesion.data
        trabajos_previos = form.trabajos_previos.data
        direccion = form.direccion.data
        comuna = form.comuna.data
        discapacidad = form.discapacidad.data
        preferencias = form.preferencias.data

        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO usuario(nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, experiencia, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad, preferencias) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [nombre,rut,fecha_aplicacion,fecha_nacimiento, nacionalidad, email, derivacion_empresa, curso_cap, nivelacion_estudio,apoyo_soclab, der_coloc, evycertif_comp, emprendimiento, apoyosocialxtra, der_orientador, seguro_cesantia, mot_derivacion, sintat_inicial, tel_not, tel_alt, experiencia, nivel_estudios, bne, plat_municipal, otro, profesion, trabajos_previos, direccion, comuna, discapacidad, preferencias])


        mysql.connection.commit()

        cur.close()

        flash("Ingresado correctamente", 'success' )
        
        return redirect(url_for('registro'))

    return render_template('register.html', form=form)    


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

        
        return send_file(filename, as_attachment=True, attachment_filename= RUT + '.docx')

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
            error = 'usuario no existe'
            return render_template('Login.html', error = error)    



    return render_template('Login.html', form = form)    





if __name__ == '__main__':
    app.run(debug = True) #este debug se tiene que borrar para la fase final solo sirve para poder recargar el sevidor

