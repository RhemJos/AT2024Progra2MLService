# AT 2024 - Progra2 MLService

## Descripción

Este proyecto es una API REST desarrollada con Flask y {insertar librerías/tecnologías} para manejar el reconocimiento de género usando imágenes, reconocer objetos en imágenes o videos y reconocimiento facial.

## Estructura del Proyecto
```
project-root/
│
├── models/
│   └── user.py
│
├── services/
│   └── user_service.py
│
├── controllers/
│   └── user_controller.py
│
├── routes/
│   ├── user_routes.py
│   └── gender_recognizer.py
│
├── utils/
│   └── file_utils.py
│
├── requirements.txt
└── app.py
```

## Instalación

1. **Clonar el Repositorio**:
   ```bash
   git clone <URL_de_tu_repositorio>
   cd AT2024Progra2MLService
   ```
2. **Crear y Activar un Entorno Virtual**:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
3. **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
## Uso
### Iniciar el Servidor
Para iniciar el servidor, ejecuta:

```bash
python app.py
```

## Endpoints
### Crear Usuario
URL: `/api/users` Método: `POST` Body:

```json
{
    "id": "user123",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123"
}
```
#### Respuesta:

```json
{
    "id": "user123",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```
### Obtener Usuarios
URL: `/api/users` Método: `GET` Respuesta:

```json
[
    {
        "id": "user123",
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
]
```
### Obtener Usuario por ID
URL: `/api/users/<user_id>` Método: `GET` Respuesta:
```json
{
    "id": "user123",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```
### Reconocimiento de Género
URL: `/api/gender_recognizer` Método: `POST` Body (form-data):

* `file`: archivo de imagen
* `accuracy`: porcentaje de precisión
* `word`: palabra a buscar
* `model`: modelo a utilizar Respuesta:

```json
{
    "success": True,
    "message": "File saved successfully",
    "file_path": "/uploads/filename.png"
}
```
### Descargar Archivo
URL: `/api/download/<filename>` Método: `GET` Respuesta: Descarga el archivo solicitado.

## Estructura del Código
### Modelos
Definen la estructura y lógica de los datos. Ejemplo: `user.py`.

### Servicios
Manejan la lógica específica del negocio. Ejemplo: `user_service.py`.

### Controladores
Responden a las acciones del usuario y coordinan las solicitudes y respuestas. Ejemplo: `user_controller.py`.

### Utilidades
Funciones auxiliares. Ejemplo: `file_utils.py`.
