from db_ops import init_db, insertar_registro, eliminar_tabla_registros, mostrar_registros, admin



db = init_db()
db.crear_tablas()
"""eliminar_tabla_registros (db)"""


# Crear o recuperar usuario
id_usuario = admin(db, "Oscar", "123")

i=3




while i>1:
    nombre = input ("Nombre: ")
    usuario = id_usuario
    tipo = input ("Tipo: ")
    tamanio = input ("Tamanio: ")
    accion = input ("Accion: ")
    direccion = input ("Direccion: ")

    insertar_registro (db,usuario, nombre,tipo, tamanio, accion, direccion, fecha=None)
    i=i-1


success, data = mostrar_registros(db)

if success:
    if isinstance(data, list):
        for reg in data:
            print(f"ID: {reg['id']}")
            print(f"Nombre: {reg['nombre']}")
            print(f"Tamaño: {reg['tamanio']}")
            print(f"Acción: {reg['accion']}")
            print(f"Dirección: {reg['direccion']}")
            print(f"Fecha: {reg['fecha']}\n")
    else:
        print(data)  # Mensaje "No hay registros"
else:
    print(f"Error: {data}")
