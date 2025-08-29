Documentación del proyecto.

YekoBackUp es una aplicación web diseñada para facilitar la creación y restauración de respaldos de información del usuario. Utiliza PostgreSQL como sistema de base de datos y se despliega mediante contenedores Docker para garantizar portabilidad y escalabilidad.

Pasos para su configuración:
(En desarrollo – esta sección se completará mañana)


Pasos para su ejecucoón: 
(En desarrollo – esta sección se completará mañana)



## Estructura del proyecto

El backend está compuesto por los siguientes archivos:

- `main.py`: Punto de entrada de la aplicación.
- `db.py`: Manejo de la conexión y estructura de la base de datos PostgreSQL.
- `db_ops.py`: Operaciones específicas sobre la base de datos.
- `ops.py`: Funciones auxiliares para la lógica del sistema.

El frontend está compuesto por archivos `.html` y `.css` que definen la interfaz de usuario.

---

## Documentación de funciones

---

### `db.py`

#### `__init__(self)`
**Descripción:** Inicializa la instancia de conexión a la base de datos PostgreSQL.  
**Parámetros:**  
- `self`: Instancia de la clase.  
**Retorna:** No retorna ningún valor.

#### `conectar(self)`
**Descripción:** Establece una conexión con la base de datos.  
**Parámetros:**  
- `self`: Instancia de la clase.  
**Retorna:** Objeto de conexión si es exitoso; `None` en caso de error.

#### `crear_tablas(self)`
**Descripción:** Crea las tablas `usuarios`, `registros` e `ingresos` en la base de datos.  
**Parámetros:**  
- `self`: Instancia de la clase.  
**Retorna:** `True` si la creación fue exitosa; `False` y la excepción si ocurrió un error.

---

### `db_ops.py`

#### `init_db()`
**Descripción:** Inicializa la base de datos y retorna la conexión como un objeto.  
**Parámetros:**  
- Ninguno.  
**Retorna:** Objeto de conexión a la base de datos.

#### `admin(db, usuario, contrasenia)`
**Descripción:** Registra un usuario en la tabla `usuarios`.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `usuario`: Nombre del usuario a registrar.  
- `contrasenia`: Contraseña del usuario.  
**Retorna:** ID del usuario si fue exitoso; `None` si ocurrió un error.

#### `insertar_registro(db, usuario, nombre, tipo, tamanio, accion, direccion, fecha)`
**Descripción:** Inserta una entrada en la tabla `registros` para respaldos o recuperaciones por usuario.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `usuario`: ID del usuario asociado.  
- `nombre`: Nombre del registro.  
- `tipo`: Tipo de registro (archivo o carpeta).  
- `tamanio`: Tamaño del archivo o carpeta.  
- `accion`: Acción realizada (respaldo o recuperación).  
- `direccion`: Ruta del archivo o carpeta.  
- `fecha`: Fecha y hora del registro.  
**Retorna:** Tupla (`True`, ID de la entrada) si fue exitoso; (`False`, mensaje de error) si ocurrió un error.

#### `eliminar_registro(db, registro_id)`
**Descripción:** Elimina la entrada correspondiente al ID indicado en la tabla `registros`.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `registro_id`: ID del registro a eliminar.  
**Retorna:** Tupla (`True`, mensaje de éxito) si fue eliminado; (`False`, mensaje de error) si no existe o hay error.

#### `eliminar_tabla_registros(db)`
**Descripción:** Elimina por completo la tabla `registros`.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
**Retorna:** Tupla (`True`, mensaje de éxito) si fue eliminada; (`False`, mensaje de error) si ocurrió un error.

#### `mostrar_registros(db, filtro_id=None)`
**Descripción:** Recupera todos los registros de la base de datos en orden descendente por fecha.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `filtro_id`: (Opcional) ID para filtrar resultados.  
**Retorna:** Tupla (`True`, lista de registros) si fue exitoso; (`False`, mensaje de error) si ocurrió un error.

#### `obtener_id_usuario(db, usuario)`
**Descripción:** Recupera el ID de un usuario según su nombre.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `usuario`: Nombre del usuario.  
**Retorna:** ID del usuario si existe; `None` si no existe.

#### `validar_usuario(db, usuario, contrasenia)`
**Descripción:** Valida un usuario comprobando su nombre y contraseña.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `usuario`: Nombre del usuario.  
- `contrasenia`: Contraseña.  
**Retorna:** ID del usuario si la combinación es correcta; `0` si no lo es.

#### `obtener_ultimo_id(db)`
**Descripción:** Recupera el valor más alto de ID en la tabla `registros`.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
**Retorna:** Último ID si fue exitoso; `0` si ocurrió un error.

#### `obtener_ruta(db, nombre)`
**Descripción:** Recupera la ruta asociada a un nombre en la tabla `registros`.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `nombre`: Nombre del registro.  
**Retorna:** Ruta si existe; "Ruta no encontrada" si no existe; "Error al obtener ruta" si ocurre un error.

#### `obtener_registro_por_nombre(db, nombre)`
**Descripción:** Recupera un registro por nombre.  
**Parámetros:**  
- `db`: Objeto de conexión a la base de datos.  
- `nombre`: Nombre del registro.  
**Retorna:** Diccionario con nombre y dirección si existe; `None` si ocurre un error.

#### `restaurar_archivo(nombre_copia, direccion_original, carpeta_backup="/host_home/Copias")`
**Descripción:** Restaura un archivo desde la carpeta de respaldo a su ubicación original.  
**Parámetros:**  
- `nombre_copia`: Nombre del archivo de respaldo.  
- `direccion_original`: Ruta original donde se restaurará el archivo.  
- `carpeta_backup`: Carpeta de respaldo (por defecto `/host_home/Copias`).  
**Retorna:** Mensaje de éxito o error según el resultado.

---

### `ops.py`

#### `obtener_tamanio(ruta)`
**Descripción:** Calcula el tamaño total de un archivo o carpeta (incluyendo subcarpetas y archivos).  
**Parámetros:**  
- `ruta`: Ruta del archivo o carpeta.  
**Retorna:** Tamaño en bytes.

#### `obtener_metadatos(ruta)`
**Descripción:** Obtiene los metadatos de un archivo o carpeta: nombre, tipo, tamaño y fecha de modificación.  
**Parámetros:**  
- `ruta`: Ruta del archivo o carpeta.  
**Retorna:** Diccionario con los metadatos; si la ruta no existe, retorna un diccionario vacío.

#### `verificar_ruta(ruta)`
**Descripción:** Verifica si una ruta existe en el sistema de archivos.  
**Parámetros:**  
- `ruta`: Ruta a verificar.  
**Retorna:** `True` si la ruta existe; `False` en caso contrario.

#### `copiar_a_documentos(ruta_origen, db)`
**Descripción:** Copia un archivo o carpeta a `/host_home/Copias`, renombrándolo con el próximo ID disponible.  
**Parámetros:**  
- `ruta_origen`: Ruta del archivo o carpeta a copiar.  
- `db`: Objeto de conexión a la base de datos.  
**Retorna:** Nombre del archivo o carpeta copiado si fue exitoso; `False` si ocurrió un error.

#### `recuperar_archivo(nombre)`
**Descripción:** (En desarrollo) Función destinada a recuperar un archivo por nombre.  
**Parámetros:**  
- `nombre`: Nombre del archivo a recuperar.  
**Retorna:** Actualmente retorna `0`.

---

### `main.py`

#### `home()`
**Descripción:** Página principal que muestra todos los registros almacenados en la base de datos.
**Ruta:** `/`  
**Métodos:** `GET`, `POST`  
**Retorna:** Renderiza la plantilla `home.html` con los registros o un mensaje de error.

#### `mostrar_recover()`
**Descripción:** Muestra la página para recuperar archivos respaldados.
**Ruta:** `/recover`  
**Métodos:** `GET`, `POST`  
**Retorna:** Renderiza la plantilla `recover.html`.

#### `login()`
**Descripción:** Muestra la página de inicio de sesión.
**Ruta:** `/login`  
**Métodos:** `GET`, `POST`  
**Retorna:** Renderiza la plantilla `login.html`.

#### `singin()`
**Descripción:** Muestra la página de registro de nuevos usuarios.
**Ruta:** `/signin`  
**Métodos:** `GET`, `POST`  
**Retorna:** Renderiza la plantilla `signin.html`.

#### `procesar_formulario()`
**Descripción:** Procesa el formulario de respaldo, copia el archivo/carpeta, obtiene metadatos y guarda el registro en la base de datos.
**Ruta:** `/procesar`  
**Métodos:** `GET`, `POST`  
**Retorna:** Redirige a la página principal si es exitoso o muestra un mensaje de error.

#### `procesar_recover()`
**Descripción:** Procesa la recuperación de archivos respaldados según el nombre proporcionado.
**Ruta:** `/ProcesarRecover`  
**Métodos:** `GET`, `POST`  
**Retorna:** Renderiza la plantilla `recover.html` con un mensaje de éxito o error.

#### `validar_credenciales()`
**Descripción:** Valida las credenciales del usuario para iniciar sesión.
**Ruta:** `/ProcesarLogin`  
**Métodos:** `GET`, `POST`  
**Retorna:** Redirige a la página principal si es exitoso o a la página de login si falla.

#### `añadir_usuario()`
**Descripción:** Registra un nuevo usuario en la base de datos.
**Ruta:** `/ProcesarSignIn`  
**Métodos:** `GET`, `POST`  
**Retorna:** Redirige a la página de login tras el registro.

#### `redireccionar_signin()`
**Descripción:** Redirige a la página de registro de usuario.
**Ruta:** `/redireccionar_signin`  
**Métodos:** `GET`, `POST`  
**Retorna:** Redirige a `/signin`.

#### `redireccionar_login()`
**Descripción:** Redirige a la página de inicio de sesión.
**Ruta:** `/redireccionar_login`  
**Métodos:** `GET`, `POST`  
**Retorna:** Redirige a `/login`.

#### `borrar_registros()`
**Descripción:** Elimina todos los registros de la base de datos.
**Ruta:** `/borrar_registros`  
**Métodos:** `GET`, `POST`  
**Retorna:** Redirige a la página principal.

#### `redireccionar_restore()`
**Descripción:** Muestra la página de restauración de archivos.
**Ruta:** `/restore`  
**Métodos:** `GET`, `POST`  
**Retorna:** Renderiza la plantilla `restore.html`.

#### `logout()`
**Descripción:** Cierra la sesión del usuario actual.
**Ruta:** `/logout`  
**Métodos:** `GET`  
**Retorna:** Redirige a la página

...existing code...

---

## Documentación del Frontend

El frontend de YekoBackUp está compuesto por archivos HTML y CSS que definen la interfaz gráfica y la experiencia de usuario. A continuación se describen los principales archivos, su propósito y los elementos que contienen:

---

### Estructura de archivos principales

- `login.html`: Página de inicio de sesión.
- `register.html`: Página de registro de nuevos usuarios.
- `home.html`: Página principal tras iniciar sesión, muestra información general y navegación.
- `respaldo.html`: Página para realizar respaldos manuales de archivos o carpetas.
- `restaurar.html`: Página para restaurar archivos respaldados.
- `historial.html`: Página que muestra el historial de respaldos y restauraciones.
- `recover.html`: Página alternativa para recuperación de archivos (versión simple).
- `signin.html`: Página alternativa de registro (versión simple).
- `style.css`, `home.css`, `styles.css`: Hojas de estilo para la personalización visual.
- Carpeta `assets/`: Imágenes y logotipos utilizados en la interfaz.

---

### Detalle de cada archivo

#### `login.html`
**Propósito:**  
Permite al usuario iniciar sesión en la aplicación.

**Elementos principales:**  
- Formulario con campos para usuario y contraseña (`name="Usuario"` y `name="Contrasenia"`).
- Botón para enviar el formulario y acceder.
- Enlaces para registrar un nuevo usuario.
- Uso de TailwindCSS para estilos y responsividad.
- Logo de la aplicación en la parte superior.

---

#### `register.html`
**Propósito:**  
Permite a nuevos usuarios crear una cuenta.

**Elementos principales:**  
- Formulario con campos para usuario, contraseña y confirmación de contraseña (`name="Usuario"`, `name="Contrasenia"`, `name="Confirmar_Contrasenia"`).
- Botón para enviar el formulario y registrarse.
- Enlace para volver a la página de inicio de sesión.
- Uso de TailwindCSS para estilos y responsividad.
- Logo de la aplicación en la parte superior.

---

#### `home.html`
**Propósito:**  
Página principal tras iniciar sesión, muestra información general, navegación y acceso a funcionalidades.

**Elementos principales:**  
- Barra de navegación con enlaces a Inicio, Aplicación (respaldo), y Cerrar Sesión.
- Sección de bienvenida con mensajes motivacionales.
- Sección de características principales (respaldo, restaurar, historial) con imágenes ilustrativas.
- Sección de tabs con información sobre tecnologías utilizadas, estructura del proyecto y funcionalidades.
- Script para cambiar el contenido de los tabs dinámicamente.
- Uso de Google Fonts y TailwindCSS para estilos.

---

#### `respaldo.html`
**Propósito:**  
Permite al usuario realizar respaldos manuales de archivos o carpetas.

**Elementos principales:**  
- Formulario para seleccionar archivos o carpetas a respaldar.
- Botón para iniciar el respaldo.
- Navegación entre respaldo, restaurar e historial.
- Uso de TailwindCSS y Font Awesome para estilos e iconos.

---

#### `restaurar.html`
**Propósito:**  
Permite al usuario restaurar archivos respaldados.

**Elementos principales:**  
- Formulario para ingresar el nombre del archivo/carpeta a restaurar.
- Botón para restaurar.
- Navegación entre respaldo, restaurar e historial.
- Uso de TailwindCSS y Font Awesome para estilos e iconos.

---

#### `historial.html`
**Propósito:**  
Muestra el historial de respaldos y restauraciones realizados por el usuario.

**Elementos principales:**  
- Tabla (o lista) con los registros de respaldos y restauraciones.
- Botón para limpiar el historial.
- Navegación entre respaldo, restaurar e historial.
- Uso de TailwindCSS y Font Awesome para estilos e iconos.

---

#### `recover.html`
**Propósito:**  
Página alternativa para recuperación de archivos (versión simple).

**Elementos principales:**  
- Formulario para ingresar el nombre del archivo a recuperar.
- Botón para recuperar.
- Mensaje de resultado de la operación.

---

#### `signin.html`
**Propósito:**  
Página alternativa de registro de usuario (versión simple).

**Elementos principales:**  
- Formulario para crear una nueva cuenta (usuario y contraseña).
- Botón para registrarse.
- Botón para ir a la página de inicio de sesión.
- Mensaje de resultado de la operación.

---

#### `style.css`, `home.css`, `styles.css`
**Propósito:**  
Definen los estilos personalizados para la aplicación.

**Elementos principales:**  
- Colores, fuentes, disposición de elementos y estilos responsivos.
- Clases personalizadas para botones, formularios, tablas y navegación.
- Adaptación para dispositivos móviles y de escritorio.

---

#### Carpeta `assets/`
**Propósito:**  
Contiene imágenes y logotipos utilizados en la interfaz.

**Elementos principales:**  
- Logos de la aplicación.
- Imágenes ilustrativas para las secciones de características y tabs.

---

### Navegación y flujo de usuario

- `/` o `/login`: Página de inicio de sesión.
- `/register` o `/signin`: Página de registro de usuario.
- `/home`: Página principal tras iniciar sesión.
- `/respaldo`: Página para realizar respaldos.
- `/restaurar` o `/recover`: Página para restaurar archivos.
- `/historial`: Página de historial de respaldos y restauraciones.

---

### Dependencias del frontend

- [TailwindCSS](https://tailwindcss.com/): Framework de utilidades CSS para estilos rápidos y responsivos.
- [Boxicons](https://boxicons.com/): Iconos vectoriales para la interfaz.
- [Google Fonts](https://fonts.google.com/): Tipografía personalizada.
- [Font Awesome](https://fontawesome.com/): Iconos adicionales para la interfaz.

---

### Notas adicionales

- El frontend utiliza plantillas Jinja2 para la integración con Flask y la inserción dinámica de datos.
- Las rutas de los formularios y enlaces están conectadas con las rutas del backend para el procesamiento de datos y navegación.
- El diseño es responsivo y está optimizado para dispositivos móviles y de escritorio.

---