# jobber service image
FROM markbnj/jobber-base:master
MAINTAINER Mark Betz <betz.mark@gmail.com>

ADD temp /usr/local/bin/jobber
ADD requirements.txt /usr/local/bin/jobber/requirements.txt

# install python dependencies
RUN cd /usr/local/bin/jobber &&\
 pip install -r requirements.txt

EXPOSE 8080

CMD /bin/bash