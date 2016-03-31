FROM ubuntu:14.04

RUN apt-get update && apt-get install -y wget curl 

RUN wget https://s3.amazonaws.com/influxdb/influxdb_0.10.3-1_amd64.deb && \
dpkg -i influxdb_0.10.3-1_amd64.deb && \
service influxdb start

RUN mkdir /opt/influxDB
ADD run.sh /opt/influxDB/run.sh
RUN chmod 0755 /opt/influxDB/run.sh
RUN ls -la /opt/influxDB/*


EXPOSE 8086

CMD ["/opt/influxDB/run.sh"]
