# jobber service base image
FROM debian:wheezy
MAINTAINER Mark Betz <betz.mark@gmail.com>

# disable annoying warnings from installers
ENV DEBIAN_FRONTEND noninteractive

# install prerequisites and utils
RUN apt-get update &&\
 apt-get install -y\
 build-essential\
 checkinstall\
 curl\
 wget\
 git\
 nano\
 vim\
 python-dev\
 python-pip

# install and configure redis
RUN cd /home &&\
 wget -q http://download.redis.io/redis-stable.tar.gz &&\
 tar xvzf redis-stable.tar.gz &&\
 cd redis-stable &&\
 make &&\
 cp src/redis-server /usr/local/bin/ &&\
 cp src/redis-cli /usr/local/bin/ &&\
 cp src/redis-benchmark /usr/local/bin/ &&\
 cp src/redis-check-aof /usr/local/bin/ &&\
 cp src/redis-check-dump /usr/local/bin/ &&\
 cd .. &&\
 rm -rf redis-stable &&\
 rm redis-stable.tar.gz &&\
 mkdir /etc/redis &&\
 mkdir -p /var/redis/6379

ADD 6379.conf /etc/redis/6379.conf

# install and configure supervisor
RUN pip install supervisor
