import os
import shutil
from datetime import datetime
from pathlib import Path
from db_ops import init_db, insertar_registro

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

def verificar_ruta(ruta):
    if not os.path.exists(ruta):
        print(f"La ruta {ruta} no existe.")
        return False
    return True


def copiar_a_documentos(ruta_origen, accion):
    
    carpeta_documentos = "/host_home/Copias"
    os.makedirs(carpeta_documentos, exist_ok=True)

    nombre = os.path.basename(ruta_origen)
    ruta_destino = os.path.join(carpeta_documentos, nombre)

    try:
        if os.path.isfile(ruta_origen):
            shutil.copy2(ruta_origen, ruta_destino)
            tipo = accion
        else:
            if os.path.exists(ruta_destino):
                shutil.rmtree(ruta_destino)
            shutil.copytree(ruta_origen, ruta_destino)
            tipo = "carpeta"
        print(f"Copiado a {ruta_destino}")
    except Exception as e:
        print(f"Error al copiar: {e}")
        return False


