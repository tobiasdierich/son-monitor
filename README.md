# son-monitor
Sonata's monitoring system gathers, analyzes performance information from NS/VNF and provides alarm notifications, based on alarm definitions which have been defined from the users. The architecture of the system is based on data exporters and a monitoring server. Data exporters sends monitoring data from NS/VNFs to monitoring server which collects, analyses, stores data and generates the appropriate notifications. In generally monitoring server consisting of a rest api interface, an alerting mechanism (based on prometheus.io), a timeseries DB and a real time notification service.


### Dependencies

 * Django==1.9.2
 * django-filter==0.12.0
 * django-rest-multiple-models==1.6.3
 * django-rest-swagger==0.3.5
 * djangorestframework==3.3.2
 * Markdown==2.6.5
 * mysqlclient==1.3.7
 * Pygments==2.1.1
 * PyYAML==3.11


### Docker support

Build Docker container image
```
sudo docker build -t sonata-monitoring .
```

Run Docker container
```
sudo docker run -d -p 8000:80 sonata-monitoring
```

###Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas (trakadasp)
 * Panos Karkazis (pkarkazis)

