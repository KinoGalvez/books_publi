# Usa la imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expone el puerto que tu aplicación Flask utiliza
EXPOSE 5000

# Define el comando para ejecutar tu aplicación
CMD ["python", "app_model.py"]