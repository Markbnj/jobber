# jobber service image
FROM markbnj/jobber-base:master
MAINTAINER Mark Betz <betz.mark@gmail.com>

ADD temp /usr/local/bin/jobber
ADD requirements.txt /usr/local/bin/jobber/requirements.txt

# install python dependencies
RUN cd /usr/local/bin/jobber &&\
 pip install -r requirements.txt

ADD start-jobber.sh /usr/local/bin/jobber/start-jobber.sh
ADD debug-api /usr/local/bin/jobber/debug-api
ADD debug-admin /usr/local/bin/jobber/debug-admin
ADD supervisord.conf /etc/supervisord.conf
ADD supervisord.debug.conf /etc/supervisord.debug.conf

CMD /usr/local/bin/jobber/start-jobber.sh