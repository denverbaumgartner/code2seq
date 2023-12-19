# Arguments
ARG BASE_IMAGE=tensorflow/tensorflow:2.1.0-gpu 

# Base image
FROM --platform=linux/amd64 ${BASE_IMAGE}

# Set up the container
WORKDIR /app

RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub

RUN apt-get update && \
    apt-get install -y python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY . /app

# Environment variables
ENV FLASK_APP=app.py

# Expose ports
EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0"]
