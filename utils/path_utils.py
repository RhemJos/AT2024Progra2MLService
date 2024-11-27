import os

def normalize_path(path: str) -> str:
    """
    Normaliza las rutas para asegurar consistencia entre sistemas operativos y entornos.
    Usa BASE_UPLOAD_PATH para asegurar que la ruta sea relativa, y no absoluta.
    """
    # Normaliza los separadores de directorios
    normalized_path = path.replace('\\', '/')

    # Obtiene el BASE_UPLOAD_PATH desde el .env (en Docker será /app/uploads, en local puede variar)
    base_path = os.getenv('BASE_UPLOAD_PATH', '/app/uploads')  # Valor por defecto si no se define en el .env

    # Si la ruta contiene el BASE_UPLOAD_PATH, lo reemplazamos para hacerla relativa
    if base_path in normalized_path:
        normalized_path = normalized_path.replace(base_path, '').lstrip('/')  # Eliminamos el prefijo

    return normalized_path
