from flask import Flask, render_template, request, redirect
from db_ops import init_db, mostrar_registros, insertar_registro, eliminar_tabla_registros, admin
from ops import verificar_ruta, obtener_tamanio, copiar_a_documentos, obtener_metadatos
from datetime import datetime
import os

app = Flask(__name__)
db = init_db()
db.crear_tablas()
usuario = 'Oscar'
contrasenia = '123'
id = admin(db, usuario, contrasenia)


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/singin', methods=['GET', 'POST'])
def singin():
    return render_template('singin.html')


###Direcciones de funciones
@app.route('/procesar', methods=['GET', 'POST'])
def procesar_formulario():
    direccion = request.form.get('direccion')
    acciones = request.form.getlist('accion') 

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
        direccion=ruta_destino,
        fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    if resultado[0]:  
        return redirect('/')
    else:
        return f"Error al guardar: {resultado[1]}", 400

@app.route('/ProcesarLogin', methods=['GET', 'POST'])
def validar_credenciales():
    return redirect('/')

@app.route('/ProcesarSignIn', methods=['GET', 'POST'])
def crear_usuario():
    return redirect('/')


@app.route('/redireccionar_signin', methods=['GET', 'POST'])
def redireccionar_singin():
    return redirect('/singin')

@app.route('/redireccionar_login', methods=['GET', 'POST'])
def redireccionar_login():
    return redirect('/login')


@app.route('/borrar_registros',  methods=['GET', 'POST'])
def borrar_registros():
    eliminar = eliminar_tabla_registros(db)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)