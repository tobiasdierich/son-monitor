#!/bin/bash
service mysql start && python /opt/Monitoring/manager/manage.py runserver 0.0.0.0:8000
