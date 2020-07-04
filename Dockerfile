#FROM python:3.8-slim
FROM jjanzic/docker-python3-opencv

WORKDIR /faceblur
ADD . /faceblur
ENV FLASK_APP fb_server.py
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD flask run --host 0.0.0.0