# 1. Usar una imagen base oficial de Python ligera
FROM python:3.11-slim

# 2. Definir el directorio donde vivirá tu código dentro del contenedor
WORKDIR /app

# 3. Copiar primero el archivo de requisitos y los instalamos
# Esto hace que el despliegue sea más rápido si no cambias las librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar todo el resto del código de tu proyecto
COPY . .

# 5. Indicarle a Google Cloud qué puerto debe usar (Cloud Run usa el 8080)
EXPOSE 8080

# 6. Comando para iniciar tu servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]