FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3.7 python3.7-dev python3.7-venv python3.7-distutils build-essential libsnappy-dev libbz2-dev net-tools curl

COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /tmp
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.7 get-pip.py

RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --upgrade setuptools
RUN python3.7 -m pip install --upgrade cython
RUN python3.7 -m pip install -r /tmp/requirements.txt

COPY ./server.py /opt/app/server.py
COPY ./example_pb2.py /opt/app/example_pb2.py
COPY ./example_pb2_grpc.py /opt/app/example_pb2_grpc.py

WORKDIR /opt/app

