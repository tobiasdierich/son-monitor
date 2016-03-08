FROM ubuntu:14.04

RUN apt-get update && apt-get -y upgrade

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-pip libmysqlclient-dev python2.7-dev libyaml-dev

# Install MySQL Server in a Non-Interactive mode. Default root password will be "1234"
RUN echo "mysql-server-5.5 mysql-server/root_password password 1234" | sudo debconf-set-selections && \
echo "mysql-server-5.5 mysql-server/root_password_again password 1234" | sudo debconf-set-selections && \
DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server-5.5 && \
service mysql restart && \
mysql -uroot -p1234 -e "CREATE DATABASE IF NOT EXISTS monitoring CHARACTER SET UTF8" && \
mysql -uroot -p1234 -e "CREATE USER  monitoringuser@localhost IDENTIFIED BY 'sonata'" && \
mysql -uroot -p1234 -e "GRANT ALL PRIVILEGES ON monitoring.* TO monitoringuser@localhost" && \
mysql -uroot -p1234 -e "FLUSH PRIVILEGES"


RUN mkdir /opt/Monitoring
COPY ./ /opt/Monitoring
RUN ls -la /opt/Monitoring/*

RUN echo $(service mysql status)

RUN pip install -r /opt/Monitoring/requirements.txt && \
service mysql restart && \
python /opt/Monitoring/manager/manage.py makemigrations && \
python /opt/Monitoring/manager/manage.py migrate

ADD run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh
RUN ls -la /opt/Monitoring/*

EXPOSE 8000 9000 9090

CMD ["/opt/Monitoring/run.sh"]
