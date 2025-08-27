from db import Database
from db_ops import eliminar_tabla_registros, init_db

def limpiar():
    db=Database()
    eliminar_tabla_registros(db)
    init_db

