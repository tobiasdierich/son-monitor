FROM ubuntu:14.04

RUN apt-get update && apt-get -y upgrade && \
apt-get install -y apache2 libapache2-mod-wsgi python-dev python-pip python-yaml nano  && \
pip install Flask pika python-influxdb


RUN mkdir -p /opt/Monitoring/prometheus && \
mkdir -p /opt/Monitoring/prometheus/alertMng && \
mkdir -p /var/www/PromCnf/PromCnf/static && \
mkdir -p /var/www/PromCnf/PromCnf/templates 

COPY ./prometheus-0.17.0rc2.linux-amd64/ /opt/Monitoring/prometheus
COPY ./sonataConf/ /opt/Monitoring/prometheus
COPY ./alertMng/ /opt/Monitoring/prometheus/alertMng
COPY ./promCnfPlugin/PromCnf.conf /etc/apache2/sites-available
COPY ./promCnfPlugin/PromCnf.wsgi /var/www/PromCnf
COPY ./promCnfPlugin/ /var/www/PromCnf/PromCnf 
RUN rm /var/www/PromCnf/PromCnf/PromCnf.wsgi     

ADD run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh && \
chown -R www-data:www-data /opt/Monitoring/prometheus && \
chmod -R g+w /opt/Monitoring/prometheus 

RUN ls -la /opt/Monitoring/*

EXPOSE 9090 9089

CMD ["/opt/Monitoring/run.sh"]
