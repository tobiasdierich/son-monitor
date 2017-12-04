FROM ubuntu:14.04

ENV GOPATH $HOME/go
ENV PATH $HOME/go/bin:/usr/local:/usr/local/go/bin$PATH

RUN apt-get update && apt-get -y upgrade && \
echo postfix postfix/mailname string 'monitoring.com' | debconf-set-selections && \
echo postfix postfix/main_mailer_type string 'Internet Site' | debconf-set-selections && \
apt-get install -y apache2 libapache2-mod-wsgi python-dev python-pip python-yaml supervisor nano mailutils curl git&& \
pip install Flask pika influxdb tornado && rm -rf /var/cache/apt /var/lib/apt/lists

RUN /usr/sbin/postconf -e inet_interfaces=loopback-only && \
    /usr/sbin/postconf -e inet_protocols=ipv4 && \
    /usr/sbin/postconf -e myhostname=localhost


RUN mkdir -p /opt/Monitoring/prometheus && \
mkdir -p /opt/Monitoring/prometheus/alertMng && \
mkdir -p /opt/Monitoring/prometheus/tornadoWS/logs && \
mkdir -p /var/www/PromCnf/PromCnf/static && \
mkdir -p /var/www/PromCnf/PromCnf/templates 

COPY ./prometheus-2.0.0.linux-amd64/ /opt/Monitoring/prometheus
#COPY ./remote_storage_adapter/ /opt/Monitoring/prometheus/remote_storage_adapter
COPY ./sonataConf/ /opt/Monitoring/prometheus
COPY ./alertMng/ /opt/Monitoring/prometheus/alertMng
COPY ./tornadoWS/ /opt/Monitoring/prometheus/tornadoWS
COPY ./promCnfPlugin/PromCnf.conf /etc/apache2/sites-available
COPY ./tornadoWS/ws_domain.conf /etc/apache2/sites-available
COPY ./tornadoWS/websocket.conf /etc/supervisor/conf.d/websocket.conf
COPY ./promCnfPlugin/PromCnf.wsgi /var/www/PromCnf
COPY ./promCnfPlugin/ /var/www/PromCnf/PromCnf 
RUN rm /var/www/PromCnf/PromCnf/PromCnf.wsgi

#RUN curl -O https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz && tar -xvf go1.8.linux-amd64.tar.gz && mv go /usr/local && chmod +x /usr/local/go

#WORKDIR /opt/Monitoring/prometheus/remote_storage_adapter
#RUN go get -d ./... && go build

ADD run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh && \
chmod 0755 /opt/Monitoring/prometheus/tornadoWS/startWS.sh && \
chown -R www-data:www-data /opt/Monitoring/prometheus && \
chmod -R g+w /opt/Monitoring/prometheus 

RUN ls -la /opt/Monitoring/* 

EXPOSE 9090 9089 8002

CMD ["/opt/Monitoring/run.sh"]