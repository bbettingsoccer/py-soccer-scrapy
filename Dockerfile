# Pull de la imagen base oficial
FROM python:3.11-slim


# setup del directorio de trabajo
WORKDIR /app

# Configuración de las variables de ambiente
# ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT_TYPE=DEV

RUN apt-get update && apt-get install -y --no-install-recommends \
    net-tools \
    iputils-ping \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8002

CMD ["uvicorn", "webscrapy.app.server.app:app", "--host", "0.0.0.0", "--port", "8002"]
#ENTRYPOINT python3 main.py