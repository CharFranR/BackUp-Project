import os
import shutil
from datetime import datetime
from pathlib import Path
from db_ops import init_db, insertar_registro, obtener_ultimo_id

def obtener_tamanio(ruta):
    """
    La función `obtener_tamanio` calcula el tamaño total de un archivo o directorio especificado por la ruta de entrada.
    
    :param ruta: El parámetro `ruta` es una cadena que representa la ruta a un archivo o directorio del que deseas calcular el tamaño. Si la ruta apunta a un archivo, la función devolverá el tamaño de ese archivo. Si la ruta apunta a un directorio, devolverá el tamaño total de todos los archivos dentro de ese directorio.
    :return: La función `obtener_tamanio` devuelve el tamaño total de un archivo si la entrada es un archivo, o el tamaño total de todos los archivos dentro del directorio si la entrada es un directorio.
    """
    if os.path.isfile(ruta):
        return os.path.getsize(ruta)
    else:
        total = 0
        for dirpath, _, filenames in os.walk(ruta):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total += os.path.getsize(fp)
        return total

def obtener_metadatos(ruta) -> dict:
    """
    La función `obtener_metadatos` recibe una ruta como entrada, verifica si la ruta existe, obtiene metadatos como nombre, tipo, tamaño y fecha de modificación del archivo o carpeta en esa ruta, y devuelve un diccionario con esta información.
    
    :param ruta: La función `obtener_metadatos` recibe una ruta (`ruta`) y devuelve un diccionario con información de metadatos sobre el archivo o carpeta en esa ruta. Los metadatos incluyen el nombre, tipo (archivo o carpeta), tamaño y fecha de última modificación.
    :return: Un diccionario que contiene información de metadatos como el nombre, tipo (archivo o carpeta), tamaño y fecha de última modificación del archivo o carpeta ubicado en la ruta especificada.
    """
    if not os.path.exists(ruta):
        print(f"La ruta {ruta} no existe.")
        return {}

    ruta_obj = Path(ruta)
    nombre = ruta_obj.name
    fecha_modificacion = datetime.fromtimestamp(ruta_obj.stat().st_mtime)

    if ruta_obj.is_file():
        tipo = "archivo"
        tamanio = ruta_obj.stat().st_size
    else:
        tipo = "carpeta"
        tamanio = obtener_tamanio(ruta) 

    return {
        "nombre": nombre,
        "tipo": tipo,
        "tamanio": tamanio,
        "fecha_modificacion": fecha_modificacion
    }


def verificar_ruta(ruta):
    """
    La función `verificar_ruta` comprueba si una ruta dada existe y devuelve un valor booleano en consecuencia.
    
    :param ruta: El parámetro "ruta" en la función "verificar_ruta" es una cadena que representa una ruta de archivo o directorio que deseas comprobar si existe. La función verifica si la ruta especificada existe en el sistema de archivos. Si la ruta no existe, imprime un mensaje indicando que la ruta no existe.
    :return: La función `verificar_ruta` devuelve un valor booleano. Devuelve `True` si la ruta especificada por el parámetro `ruta` existe, y `False` si la ruta no existe.
    """
    if not os.path.exists(ruta):
        print(f"La ruta {ruta} no existe.")
        return False
    return True


def copiar_a_documentos(ruta_origen, db):
    """
    Copia un archivo o carpeta a la carpeta de documentos de respaldo, agregando un sufijo con el próximo ID disponible.
    
    :param ruta_origen: Ruta del archivo o carpeta a copiar.
    :param db: Objeto de base de datos para obtener el último ID.
    :return: El nombre del archivo o carpeta copiado, o False si ocurre un error.
    """
    try:
        ultimo_id = obtener_ultimo_id(db)
    except Exception as e:
        print(f"Error al obtener ID: {e}")
        return False

    proximo_id = ultimo_id + 1

    carpeta_documentos = "/host_home/Copias"
    os.makedirs(carpeta_documentos, exist_ok=True)
    
    nombre = os.path.basename(ruta_origen)
    nombre_sin_ext, ext = os.path.splitext(nombre)
    nombre = f"{nombre_sin_ext}_{proximo_id}{ext}"

    ruta_destino = os.path.join(carpeta_documentos, nombre)

    try:
        if os.path.isfile(ruta_origen):
            shutil.copy2(ruta_origen, ruta_destino)
        else:
            if os.path.exists(ruta_destino):
                shutil.rmtree(ruta_destino)
            shutil.copytree(ruta_origen, ruta_destino)
        return nombre
    except Exception as e:
        print(f"Error al copiar: {e}")
        return False
    
def restaurar_archivo(nombre_copia, direccion_original, carpeta_backup="/host_home/Copias"):
    """
    Esta función restaura un archivo desde una carpeta de respaldo a su ubicación original.
    
    :param nombre_copia: Nombre del archivo de copia que se desea restaurar.
    :param direccion_original: Ruta original donde se restaurará el archivo.
    :param carpeta_backup: Carpeta donde se almacenan las copias de respaldo. Por defecto es "/host_home/Copias".
    :return: Mensaje indicando si el archivo fue restaurado correctamente o si ocurrió un error. Si el archivo no existe en el respaldo, retorna un mensaje indicándolo. Si ocurre un error, retorna un mensaje con el error.
    """
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