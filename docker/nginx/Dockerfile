FROM ubuntu:18.04

RUN apt-get update && apt-get install -y build-essential wget libssl-dev zlib1g-dev
RUN mkdir /root/work
WORKDIR /root/work
RUN wget https://nginx.org/download/nginx-1.17.8.tar.gz && tar zxvf nginx-1.17.8.tar.gz
RUN cd nginx-1.17.8 \
    && ./configure --prefix=/usr/local --with-http_ssl_module --with-http_v2_module --without-http_rewrite_module \
    && make -j4 && make install
COPY docker/nginx/conf.d/nginx.conf /usr/local/conf/nginx.conf
RUN rm -rf nginx-1.17.8*

WORKDIR /opt

CMD ["nginx", "-g", "daemon off;"]
