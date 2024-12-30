# Pull de la imagen base oficial
FROM python:3.11-alpine


# setup del directorio de trabajo
WORKDIR /app

# Configuración de las variables de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8004:8004/tcp

ENTRYPOINT python3 src/main.py