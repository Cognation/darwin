FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip curl git && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get install -y python3-pip

WORKDIR /app
VOLUME /app/data

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x build.sh
RUN ./build.sh

EXPOSE 80

ENV NAME Darwin

CMD ["python", "server.py", "--port", "80"]

# sudo docker run --env-file .env -v ./data:/app/data -p 8080:80 darwin