from flask import Flask, render_template, request, redirect, session
from db import Database
from db_ops import crear_usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_super_secreta_123'

# Inicializar DB y tablas
db = Database()
db.crear_tablas()

# Usuario por defecto
crear_usuario(db, "Oscar", "123")

# ----------------- Rutas -----------------

@app.route('/')
def index():
    if "usuario" in session:
        return render_template('home.html', usuario=session["usuario"])
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/procesar_login', methods=['POST'])
def procesar_login():
    usuario = request.form.get('usuario', '').strip()
    contrasena = request.form.get('contrasena', '').strip()

    try:
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT contrasenia FROM usuarios WHERE usuario = %s", (usuario,))
                user = cur.fetchone()

        if user and user[0] == contrasena:
            session["usuario"] = usuario
            return redirect('/')
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"Error en login: {e}")
        return render_template('login.html', error="Error interno")

@app.route('/singin')
def singin():
    return render_template('singin.html')

@app.route('/procesar_singin', methods=['POST'])
def procesar_singin():
    usuario = request.form.get('usuario').strip()
    contrasena = request.form.get('contrasena').strip()
    confirmar = request.form.get('confirmar').strip()

    if contrasena != confirmar:
        return render_template('singin.html', error="Las contraseñas no coinciden")

    if crear_usuario(db, usuario, contrasena):
        return redirect('/login')
    else:
        return render_template('singin.html', error="Error al crear usuario " + usuario + " " + contrasena + " " + confirmar)

@app.route('/logout')
def logout():
    session.pop("usuario", None)
    return redirect('/login')

@app.route('/redireccionar_singin', methods=['POST'])
def redireccionar_singin():
    return redirect('/singin')

# ----------------- Inicio -----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
