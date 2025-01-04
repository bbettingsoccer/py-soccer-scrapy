# Pull de la imagen base oficial
FROM python:3.11-alpine


# setup del directorio de trabajo
WORKDIR /app

# Configuración de las variables de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8004:8004/tcp
CMD [“uvicorn”, “main:app”, “ — host”, “0.0.0.0”, “ — port”, “8000”, “ — reload”]
ENTRYPOINT python3 src/main.py