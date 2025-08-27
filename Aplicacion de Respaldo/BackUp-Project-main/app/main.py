from flask import Flask, render_template, request, redirect, session
from db_ops import init_db, mostrar_registros, insertar_registro, eliminar_tabla_registros, admin, obtener_ruta, restaurar_archivo, validar_usuario, obtener_registro_por_nombre
from ops import verificar_ruta, copiar_a_documentos, obtener_metadatos
from datetime import datetime
import os

app = Flask(__name__)
db = init_db()
db.crear_tablas()
usuario = 'Oscar'
contrasenia = '123'
id = admin(db, usuario, contrasenia)

app.secret_key = "una_clave_secreta_segura"

###Paginas visitables
@app.route('/', methods=['GET', 'POST'])

def home():
    success, data = mostrar_registros(db)
    
    if not success:
        return f"Error: {data}", 500
    
    if data == None:
        return f"Sin Data", 500
        
    registros = data if isinstance(data, list) else []

    return render_template('home.html', registros=data)

@app.route('/recover', methods=['GET', 'POST'])

def mostrar_recover():
    return render_template('recover.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def singin():

    return render_template('signin.html')

@app.route('/respaldo', methods=['GET', 'POST'])
def respaldo():
    return render_template('respaldo.html')

@app.route('/historial', methods=['GET', 'POST'])
def historial():
    return render_template('historial.html')

###Direcciones de funciones
@app.route('/procesar', methods=['GET', 'POST'])
def procesar_formulario():
    direccion = request.form.get('direccion')

    validar = verificar_ruta(direccion)
    if not validar:
        return "Ruta no válida", 400
    

    # 1. Copiar primero con nombre modificado
    nombre_nuevo = copiar_a_documentos(direccion, db)
    if not nombre_nuevo:
        return "Error al copiar", 400

    # 2. Ruta destino ya copiada
    carpeta_documentos = "/host_home/Copias"
    ruta_destino = os.path.join(carpeta_documentos, nombre_nuevo)

    # 3. Ahora obtienes los metadatos de ese archivo renombrado
    metadatos = obtener_metadatos(ruta_destino)
    if not metadatos:
        return "No se pudieron obtener metadatos", 400

    nombre = metadatos.get("nombre")
    tamanio = metadatos.get("tamanio")
    tipo = metadatos.get("tipo")

    # 4. Guardar en BD con el nombre ya renombrado
    resultado = insertar_registro(
        db=db,
        usuario=id,
        nombre=nombre,
        tipo=tipo,
        tamanio=tamanio,
        accion="respaldo",
        direccion=direccion,
        fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    if resultado[0]:  
        return redirect('/')
    else:
        return f"Error al guardar: {resultado[1]}", 400
    

@app.route('/ProcesarRecover', methods=[ 'GET','POST'])
def procesar_recover():
    nombre = request.form.get('nombre')  # O 'Nombre' según el form
    registro = obtener_registro_por_nombre(db, nombre)

    if registro:
        mensaje = restaurar_archivo(
            nombre_copia=registro['nombre'],
            direccion_original=registro['direccion']
        )
    else:
        mensaje = "No se encontró el registro"

    return render_template('recover.html', mensaje=mensaje)

@app.route('/ProcesarLogin', methods=['GET', 'POST'])
def validar_credenciales():

    usuario = request.form.get('Usuario')
    contrasenia = request.form.get('Contrasenia')
    validacion = validar_usuario (db,usuario,contrasenia)

    if validacion != 0:
        session['usuario'] = usuario
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/ProcesarSignIn', methods=['GET', 'POST'])
def añadir_usuario():
    usuario = request.form.get('Usuario')
    contrasenia = request.form.get('Contrasenia')
    id = admin(db,usuario,contrasenia)
    return redirect('/login')

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