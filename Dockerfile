
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
RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y ffmpeg
RUN apt-get install -y wget curl
RUN curl -sSL https://install.python-poetry.org/ | python -


RUN mkdir model
RUN wget -P ./model/ ${URL_MODEL}
# RUN mv ./model/

COPY ./ ./
# COPY ./requirements.txt ./
# RUN ${HOME}/.local/bin/poetry install --no-dev
RUN ${HOME}/.local/bin/poetry install --no-root

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN pip install git+https://github.com/kevin-tofu/MediaHandler.git@master
# RUN pip install git+https://github.com/kevin-tofu/coco_formatter.git@main

# -e git+https://github.com/kevin-tofu/MediaHandler.git#egg=v0.0.1
ENV http_proxy=
ENV https_proxy=

EXPOSE 80

# CMD ["python", "./server.py"]
CMD ["${home}/.local/bin/poetry", "run", "python", "./server.py"]
