#!/bin/bash
echo "Wait 10 secs...."
sleep 10 && \
python /opt/Monitoring/manage.py makemigrations && \
python /opt/Monitoring/manage.py migrate && \
python /opt/Monitoring/manage.py collectstatic --noinput && \
echo "from django.contrib.auth.models import User; User.objects.create_superuser('user', 'user@mail.com', 'sonat@')" | python /opt/Monitoring/manage.py shell && \
mv /opt/Monitoring/apache-site /etc/apache2/sites-available/000-default.conf && \
sed -i.bak 's/.*Listen.*/Listen '8000'/' /etc/apache2/ports.conf && \
chown -R www-data:www-data /opt/Monitoring && \
service apache2 restart 
tail -f /dev/null
#/opt/Monitoring/manage.py runserver 0.0.0.0:8000

#./opt/Monitoring/prometheus-0.17.0rc2.linux-amd64/prometheus -config.file=/opt/Monitoring/prometheus-0.17.0rc2.linux-amd64/prometheus.yml >/dev/null 2>&1 &
#service mysql start python && /opt/Monitoring/manager/manage.py runserver 0.0.0.0:8000
