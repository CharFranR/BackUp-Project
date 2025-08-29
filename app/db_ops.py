from db import Database
from datetime import datetime
import os 
import shutil

def init_db():
    """
    La función `init_db` inicializa una conexión a la base de datos retornando un objeto `Database`.
    :return: Se retorna una instancia de la clase `Database`.
    """
    return Database()

def admin(db, usuario, contrasenia):
    """
    La función `admin` intenta insertar un nuevo usuario en la base de datos, retornando el ID del usuario si tiene éxito.
    
    :param db: El parámetro `db` es un objeto que representa la conexión o sesión a la base de datos. Se utiliza para ejecutar consultas y confirmar transacciones.
    :param usuario: El parámetro `usuario` representa el nombre de usuario que se desea insertar o recuperar de la base de datos.
    :param contrasenia: El parámetro `contrasenia` representa la contraseña del usuario que se está agregando o verificando en la base de datos.
    :return: La función retorna el `id` del usuario si ya existe o si se inserta correctamente. Si ocurre un error, retorna `None`.
    """
    try:
        id_usuario = obtener_id_usuario(db, usuario)
        if id_usuario:
            return None  # Usuario ya existe, no permitir duplicados
        query = """
        INSERT INTO usuarios (usuario, contrasenia)
        VALUES (%s, %s)
        RETURNING id
        """
        with db.conectar () as conn:
            with conn.cursor() as cur:
                cur.execute(query, (usuario, contrasenia))
                registro_id = cur.fetchone()[0]
                conn.commit()
        return registro_id

    except Exception as e:
        print(f"Error al insertar registro: {e}")
        return None

def insertar_registro(db, usuario, nombre, tipo,  tamanio, accion, direccion, fecha):
    """
     La función `insertar_registro` inserta un nuevo registro en la base de datos con los valores especificados y retorna el ID del registro insertado.
    
    :param db: Objeto de conexión a la base de datos.
    :param usuario: ID del usuario asociado al registro.
    :param nombre: Nombre del registro o entrada a insertar.
    :param tipo: Tipo del registro (por ejemplo, "documento", "imagen", etc.).
    :param tamanio: Tamaño del dato almacenado (por ejemplo, tamaño del archivo en bytes).
    :param accion: Acción asociada al registro (por ejemplo, 'crear', 'actualizar', 'eliminar').
    :param direccion: Dirección o ubicación asociada al registro.
    :param fecha: Fecha y hora del registro, en formato '%Y-%m-%d %H:%M:%S'.
    :return: Una tupla con un booleano indicando éxito (True) o error (False), y el ID insertado o mensaje de error.
    """
    try:
        query = """
        INSERT INTO registros (nombre, id_usuarios, tipo, tamanio, accion, direccion, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        fecha_parsed = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S') if fecha else None
        
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (nombre, usuario, tipo, tamanio, accion, direccion, fecha_parsed))
                registro_id = cur.fetchone()[0]
                conn.commit()
                
        return (True, registro_id)
        
    except Exception as e:
        error_msg = f"Error al insertar registro: {e}"
        print(error_msg)
        return (False, error_msg)
    
def eliminar_registro(db, registro_id):
    """
    Esta función elimina un registro de la base de datos según el ID proporcionado y retorna un mensaje de éxito si se elimina correctamente.
    
    :param db: Objeto de conexión a la base de datos.
    :param registro_id: Identificador único del registro a eliminar.
    :return: Una tupla con un booleano y un mensaje. Si se elimina, el mensaje incluye el nombre y el ID del registro. Si no existe, retorna un mensaje diferente. Si ocurre una excepción, retorna un mensaje de error.
    """
    try:
        query = "DELETE FROM registros WHERE id = %s RETURNING nombre"
        
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (registro_id,))
                resultado = cur.fetchone()
                conn.commit()
                
                if resultado:
                    return (True, f"Registro '{resultado[0]}' (ID: {registro_id}) eliminado")
                return (False, "El registro no existe")
                
    except Exception as e:
        error_msg = f"Error al eliminar registro: {e}"
        print(error_msg)
        return (False, error_msg)

 
def eliminar_tabla_registros(db):
    """
    La función `eliminar_tabla_registros` intenta eliminar la tabla 'registros' de la base de datos y retorna un mensaje de éxito si la operación es exitosa.
    
    :param db: Objeto de conexión a la base de datos.
    :return: Una tupla con un booleano y un mensaje. Si la tabla se elimina correctamente, retorna `(True, "Tabla 'registros' eliminada exitosamente")`. Si ocurre un error, retorna `(False, error_msg)`.
    """
    try:
        with db.conectar() as conn:
            with conn.cursor() as cur:
                
                cur.execute("DROP TABLE IF EXISTS registros CASCADE")
                conn.commit()
                
        return (True, "Tabla 'registros' eliminada exitosamente")
        
    except Exception as e:
        error_msg = f"Error al eliminar tabla: {e}"
        print(error_msg)
        return (False, error_msg)


def mostrar_registros(db, filtro_id=None):
    """
    La función `mostrar_registros` recupera registros de la base de datos y los retorna en orden descendente por fecha.
    
    :param db: Objeto de conexión a la base de datos.
    :param filtro_id: (Opcional) Filtro por ID.
    :return: Una tupla. El primer elemento es un booleano indicando éxito (True) o error (False). El segundo elemento es una lista de diccionarios con los registros recuperados o un mensaje de error.
    if successful, or an error message if an exception occurred during the process.
    """
   
    try:
        query = """
        SELECT nombre, tipo, tamanio, fecha, direccion
        FROM registros
        WHERE id_usuarios = %s
        ORDER BY fecha DESC
        """
        params = (filtro_id,)
            
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                registros = cur.fetchall()

                if not registros:
                    return (True, []) 

                column_names = [desc[0] for desc in cur.description]
                
                resultados = []
                for reg in registros:
                    resultados.append(dict(zip(column_names, reg)))
                
                return (True, resultados)
                
    except Exception as e:
        return (False, f"Error al leer registros: {e}")
    
def registar_recuperacion(db, nombre):
    try:
        query = """
        INSERT INTO recuperaciones (nombre, fecha)
        VALUES (%s,  CURRENT_TIMESTAMP)
        RETURNING id
        """
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (nombre, ))
                recuperacion_id = cur.fetchone()[0]
                conn.commit()
        return (True, recuperacion_id)
    except Exception as e:
        error_msg = f"Error al insertar registro de recuperación: {e}"
        print(error_msg)
        return (False, error_msg)


def mostrar_recuperaciones (db, filtro_id=None):
    try:
        query = """
        SELECT nombre, fecha
        FROM recuperaciones
        ORDER BY fecha DESC
        """
        params = ()

        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                recuperaciones = cur.fetchall()

                if not recuperaciones:
                    return (True, [])
                column_names = [desc[0] for desc in cur.description]

                resultados = []
                for reg in recuperaciones:
                    resultados.append(dict(zip(column_names, reg)))
                return (True, resultados)

    except Exception as e:
        return (False, f"Error al leer recuperaciones: {e}")

def obtener_id_usuario(db, usuario):
    """
    La función `obtener_id_usuario` recupera el ID de un usuario de la base de datos según el nombre de usuario proporcionado.
    
    :param db: Objeto de conexión a la base de datos.
    :param usuario: Nombre de usuario a buscar.
    :return: El ID del usuario si existe, de lo contrario retorna `None`.
    """
    query = "SELECT id FROM usuarios WHERE usuario = %s"
    with db.conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (usuario,))
            result = cur.fetchone()
        if result:
            return result[0]
        return None
    
def validar_usuario (db, usuario, contrasenia):
    """
    Esta función valida un usuario comprobando su nombre y contraseña en la base de datos.
    
    :param db: Objeto de conexión a la base de datos.
    :param usuario: Nombre de usuario.
    :param contrasenia: Contraseña.
    :return: El ID del usuario si la combinación es correcta, de lo contrario retorna 0.
    """
    query = """
    SELECT id
    FROM usuarios 
    WHERE usuario = %s AND contrasenia = %s
    """
    with db.conectar() as conn:
        with conn.cursor () as cur:
            cur.execute(query, (usuario, contrasenia))
            resultado = cur.fetchone()
            return resultado [0] if resultado else None

    

def obtener_ultimo_id(db):
    """
    La función `obtener_ultimo_id` recupera el valor más alto de ID de la tabla `registros` en la base de datos, manejando excepciones y retornando 0 si ocurre un error.
    
    :param db: Objeto de conexión a la base de datos.
    :return: El último ID de la tabla "registros". Si ocurre un error, retorna 0.
    """
    try:
        query = "SELECT COALESCE(MAX(id), 0) FROM registros"
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                resultado = cur.fetchone()
                return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error al obtener último ID: {e}")
        return 0
    

def obtener_ruta (db,nombre):
    """
    La función "obtener_ruta" recupera la dirección asociada a un nombre dado desde la base de datos.
    
    :param db: Objeto de conexión a la base de datos.
    :param nombre: Nombre del registro para obtener la ruta (dirección).
    :return: La dirección correspondiente al nombre dado si se encuentra. Si no existe, retorna "Ruta no encontrada". Si ocurre una excepción, retorna "Error al obtener ruta".
    """
    try:
        query = """
        SELECT direccion
        FROM registros 
        WHERE nombre = %s;
        """
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (nombre,))
                resultado = cur.fetchone()
                return resultado[0] if resultado else "Ruta no encontrada"
    except Exception as e:
        print(f"Error al obtener ruta: {e}")
        return "Error al obtener ruta"
    
def obtener_registro_por_nombre(db, nombre):
    """
     La función `obtener_registro_por_nombre` recupera un registro de la base de datos por nombre.
    
    :param db: Objeto de conexión a la base de datos.
    :param nombre: Nombre del registro a buscar.
    :return: Si la consulta es exitosa y se encuentra el registro, retorna un diccionario con el nombre y la dirección. Si ocurre un error, retorna None.
    """
    try:
        query = """
        SELECT nombre, direccion
        FROM registros
        WHERE nombre = %s;
        """
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (nombre,))
                row = cur.fetchone()
                if row:
                    return {"nombre": row[0], "direccion": row[1]}
    except Exception as e:
        print(f"Error al obtener registro: {e}")
    return None

def registrar_ingreso(db, usuario_id):
    """
    Registra un ingreso (inicio de sesión) en la tabla ingresos.
    :param db: Objeto de conexión a la base de datos.
    :param usuario_id: ID del usuario que inicia sesión.
    :return: True si se registró correctamente, False en caso de error.
    """
    try:
        query = """
        INSERT INTO ingresos (id_usuarios, fecha)
        VALUES (%s, CURRENT_TIMESTAMP)
        """
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (usuario_id,))
                conn.commit()
        return True
    except Exception as e:
        print(f"Error al registrar ingreso: {e}")
        return False