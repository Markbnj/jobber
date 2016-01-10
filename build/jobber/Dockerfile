# jobber service image
FROM markbnj/jobber-base:master
MAINTAINER Mark Betz <betz.mark@gmail.com>

ADD code /usr/local/bin/jobber
ADD start-jobber.sh /usr/local/bin/jobber/
ADD jobber.yml /etc/jobber/
ADD debug-api /usr/local/bin/jobber/
ADD debug-admin /usr/local/bin/jobber/
ADD supervisord.conf /etc/
ADD supervisord.debug.conf /etc/

CMD /usr/local/bin/jobber/start-jobber.sh