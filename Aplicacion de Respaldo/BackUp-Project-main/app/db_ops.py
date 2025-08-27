from db import Database
from datetime import datetime
import os 
import shutil

def init_db():
    """Inicializa la conexión a la base de datos"""
    return Database()

def admin(db, usuario, contrasenia):
    try:
        id_usuario = obtener_id_usuario(db, usuario)
        if id_usuario:
            return id_usuario
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
   
    try:
        query = """
        SELECT *
        FROM registros
        ORDER BY fecha DESC
        """
        params = ()
            
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                registros = cur.fetchall()

                if not registros:
                    return (True, []) 

                column_names = [desc[0] for desc in cur.description]
                
                if not registros:
                    return (True, "No hay registros encontrados")
                
                resultados = []
                for reg in registros:
                    resultados.append(dict(zip(column_names, reg)))
                
                return (True, resultados)
                
    except Exception as e:
        return (False, f"Error al leer registros: {e}")
    

def obtener_id_usuario(db, usuario):
    query = "SELECT id FROM usuarios WHERE usuario = %s"
    with db.conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (usuario,))
            result = cur.fetchone()
        if result:
            return result[0]
        return None
    
def validar_usuario (db, usuario, contrasenia):
    query = """
    SELECT id
    FROM Usuarios 
    WHERE usuario = %s AND contrasenia = %s
    """
    with db.conectar() as conn:
        with conn.cursor () as cur:
            cur.execute(query, (usuario, contrasenia))
            resultado = cur.fetchone()
            return resultado [0] if resultado else 0

    

def obtener_ultimo_id(db):
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


def restaurar_archivo(nombre_copia, direccion_original, carpeta_backup="/host_home/Copias"):
    import os, shutil
    try:
        origen = os.path.join(carpeta_backup, nombre_copia)
        carpeta_destino = os.path.dirname(direccion_original)

        if not os.path.exists(origen):
            return f"No existe en backup: {origen}"

        os.makedirs(carpeta_destino, exist_ok=True)
        shutil.copy(origen, carpeta_destino)
        return f"Archivo restaurado en {carpeta_destino}"
    except Exception as e:
        return f"Error al restaurar archivo: {e}"