
ARG registry=fukouhei001
# FROM ${registry}/opencv-python3-8:v1
# FROM node:12.13.0-alpine as build
# FROM python:3.8-slim-buster
FROM python:3.10-slim-buster
ARG URL_MODEL="https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_m.onnx"
# ARG HTTP_PROXY=""
# ARG HTTPS_PROXY=""
# ARG fpath_model="./model/yolox_m.onnx"

# ENV http_proxy HTTP_PROXY
# ENV https_proxy HTTPS_PROXY

WORKDIR /myapp
COPY ./ ./

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y ffmpeg
RUN apt-get install -y wget curl
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org/  | python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN mkdir model
RUN wget -O ./model/yolo.onnx ${URL_MODEL}


RUN poetry install --no-root
ENV http_proxy=
ENV https_proxy=

EXPOSE 80

CMD ["python", "./server.py"]