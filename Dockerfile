# PYTHON 11 BASE IMAGE
FROM python:3.11-slim

WORKDIR /app
VOLUME /app/data

COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    git
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME Darwin

CMD ["python", "server.py", "--port", "80"]

# sudo docker run --env-file .env -v ./data:/app/data -p 8080:80 darwin