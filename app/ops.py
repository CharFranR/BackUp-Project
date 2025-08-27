import os
import shutil
from datetime import datetime
from pathlib import Path
from db_ops import init_db, insertar_registro, obtener_ultimo_id

def obtener_tamanio(ruta):
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
    if not os.path.exists(ruta):
        print(f"La ruta {ruta} no existe.")
        return False
    return True


def copiar_a_documentos(ruta_origen, db):
    """
    Copia un archivo o carpeta a /host_home/Copias,
    renombrándolo con el próximo ID disponible.
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
    

def recuperar_archivo(nombre):

    


    return 0