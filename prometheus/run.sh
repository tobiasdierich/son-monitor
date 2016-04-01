#!/bin/bash
/opt/Monitoring/prometheus/prometheus -config.file=/opt/Monitoring/prometheus/prometheus.yml -storage.local.retention 680h0m0s  -storage.remote.influxdb-url http://influx:8086 -storage.remote.influxdb.database "prometheus" -storage.remote.influxdb.retention-policy "default" >/dev/null 2>&1

