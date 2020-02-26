FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3.7 python3.7-dev python3.7-venv python3.7-distutils
RUN apt-get install -y build-essential libsnappy-dev libbz2-dev
RUN apt-get install -y git curl

COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /tmp

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.7 get-pip.py
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --upgrade setuptools
RUN python3.7 -m pip install --upgrade cython
RUN python3.7 -m pip install -r /tmp/requirements.txt

# install supervisor for Python3.7
RUN git clone https://github.com/Supervisor/supervisor.git
RUN cd supervisor && python3.7 setup.py install
RUN rm -rf supervisor
RUN mkdir -p /var/log/supervisor
COPY ./docker/grpc/conf.d/supervisord.conf /etc/supervisor/supervisord.conf

COPY ./server.py /opt/app/server.py
COPY ./example_pb2.py /opt/app/example_pb2.py
COPY ./example_pb2_grpc.py /opt/app/example_pb2_grpc.py

WORKDIR /opt/app

