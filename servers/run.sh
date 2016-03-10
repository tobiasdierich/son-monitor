#!/bin/bash
./opt/Monitoring/prometheus-0.17.0rc2.linux-amd64/prometheus -config.file=/opt/Monitoring/prometheus-0.17.0rc2.linux-amd64/prometheus.yml >/dev/null 2>&1 &
service mysql start && python /opt/Monitoring/manager/manage.py runserver 0.0.0.0:8000
