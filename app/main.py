from flask import Flask, render_template, request, redirect, session
from db_ops import *
from ops import obtener_metadatos, restaurar_archivo
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
db = init_db()
db.crear_tablas()

app.secret_key = "una_clave_secreta_segura"

###Paginas visitables
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/respaldo', methods=['GET', 'POST'])
def mostrar_recover():
    return render_template('respaldo.html')

@app.route('/restaurar', methods=['GET', 'POST'])
def restaurar():

    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect('/')

    success, data = mostrar_recuperaciones(db, filtro_id=None)
    
    if not success:
        return f"Error: {data}", 500
    
    recuperaciones = data if isinstance(data, list) else []

    return render_template('restaurar.html', recuperaciones=recuperaciones)

@app.route('/historial', methods=['GET', 'POST'])
def historial():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect('/')

    success, data = mostrar_registros(db, filtro_id=usuario_id)
    
    if not success:
        return f"Error: {data}", 500
    
    registros = data if isinstance(data, list) else []
    return render_template('historial.html', registros=registros)

###Direcciones de funciones
@app.route('/procesar', methods=['GET', 'POST'])
def procesar_formulario():

    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect('/login')

    if 'archivo' not in request.files:
        return "No se envió ningún archivo", 400

    # 🔹 Ahora puede ser un archivo o varios
    archivos = request.files.getlist('archivo')
    if not archivos or all(not a.filename for a in archivos):
        return "No se seleccionó ningún archivo", 400

    for archivo in archivos:
        if archivo and archivo.filename:
            nombre_archivo_original = secure_filename(archivo.filename)
            nombre_sin_ext, ext = os.path.splitext(nombre_archivo_original)

            # 1. Obtener el próximo ID
            proximo_id = obtener_ultimo_id(db) + 1

            # 2. Renombrar el archivo al formato nombre_id.ext
            nombre_archivo_backup = f"{nombre_sin_ext}_{proximo_id}{ext}"

            carpeta_destino = "/host_home/Copias"
            os.makedirs(carpeta_destino, exist_ok=True)
            ruta_destino = os.path.join(carpeta_destino, nombre_archivo_backup)
            archivo.save(ruta_destino)

            # 3. Obtener metadatos del archivo guardado
            metadatos = obtener_metadatos(ruta_destino)
            if not metadatos:
                continue  # si falla un archivo, seguimos con los demás

            nombre = nombre_archivo_backup
            tamanio = metadatos.get("tamanio")
            tipo = metadatos.get("tipo")

            # 4. Guardar en la base de datos
            insertar_registro(
                db=db,
                usuario=usuario_id,
                nombre=nombre,  # nombre_id.ext
                tipo=tipo,
                tamanio=tamanio,
                accion="respaldo",
                direccion=f"/host_documents/{nombre_archivo_original}",  # ruta original simulada
                fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

    # 🔹 Al terminar todos, redirigir
    return redirect('/respaldo')
    

@app.route('/ProcesarRecover', methods=[ 'GET','POST'])
def procesar_recover():
    nombre = request.form.get('nombre') 
    registro = obtener_registro_por_nombre(db, nombre)

    if registro:
        restaurar_archivo(
            nombre_copia=registro['nombre'],
            direccion_original=registro['direccion']
        )

        registar_recuperacion(db, nombre)
    else:
        mensaje = "No se encontró el registro"

    return redirect('/restaurar')

@app.route('/ProcesarLogin', methods=['GET', 'POST'])
def validar_credenciales():
    usuario = request.form.get('Usuario')
    contrasenia = request.form.get('Contrasenia')
    id_usuario = validar_usuario(db, usuario, contrasenia)

    if id_usuario:
        session['usuario_id'] = id_usuario 
        registrar_ingreso(db, id_usuario)
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/ProcesarRegister', methods=['GET', 'POST'])
def añadir_usuario():
    usuario = request.form.get('Usuario')
    contrasenia = request.form.get('Contrasenia')
    confirmar_contrasenia = request.form.get('Confirmar_Contrasenia')

    if contrasenia != confirmar_contrasenia:
        return "Las contraseñas no coinciden", 400
    id = admin(db,usuario,contrasenia)
    return redirect('/')



@app.route('/redireccionar_signin', methods=['GET', 'POST'])
def redireccionar_signin():
    return redirect('/signin')

@app.route('/redireccionar_login', methods=['GET', 'POST'])
def redireccionar_login():
    return redirect('/login')


@app.route('/borrar_registros',  methods=['GET', 'POST'])
def borrar_registros():
    eliminar = eliminar_tabla_registros(db)
    return redirect('/')


@app.route('/restore', methods=['GET', 'POST'])
def redireccionar_restore():
    return render_template('restore.html')

@app.route('/logout')
def logout():
    session.pop("usuario", None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)