# Pull de la imagen base oficial
FROM python:3.11-alpine


# setup del directorio de trabajo
WORKDIR /src

# Configuración de las variables de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT_TYPE DEV

RUN pip install --upgrade pip
COPY requirements.txt /src/
RUN pip install -r requirements.txt

EXPOSE 8004:8004/tcp


COPY py-soccer-scrapy/src ./src/

ENTRYPOINT python3 src/app/server/main.py