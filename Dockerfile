
ARG registry=fukouhei001
# FROM ${registry}/opencv-python3-8:v1
# FROM node:12.13.0-alpine as build
FROM python:3.8-slim-buster
ARG URL_MODEL="https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_m.onnx"
# ARG fpath_model="./model/yolox_m.onnx"

WORKDIR /myapp
RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt install -y ffmpeg
RUN mkdir model
RUN wget -P ./model/ ${URL_MODEL}
# RUN mv ./model/

COPY ./ ./
COPY ./requirements.txt ./
RUN apt-get install -y git

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/kevin-tofu/MediaHandler.git@master
RUN pip install git+https://github.com/kevin-tofu/coco_formatter.git@main

# -e git+https://github.com/kevin-tofu/MediaHandler.git#egg=v0.0.1
ENV http_proxy=
ENV https_proxy=

EXPOSE 80

CMD ["python", "./server.py"]
