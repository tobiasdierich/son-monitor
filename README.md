# son-monitor [![Build Status](http://jenkins.sonata-nfv.eu/buildStatus/icon?job=son-monitor)](http://jenkins.sonata-nfv.eu/job/son-monitor)
Sonata's monitoring system gathers, analyzes performance information from NS/VNF and provides alarm notifications, based on alarm definitions which have been defined from the users. The architecture of the system is based on data exporters and a monitoring server. Data exporters sends monitoring data from NS/VNFs to monitoring server which collects, analyses, stores data and generates the appropriate notifications. In generally monitoring server consisting of a rest api interface, an alerting mechanism (based on prometheus.io), a timeseries DB and a real time notification service.

### Dependencies
 * Docker compose
 * Django==1.9.2
 * django-filter==0.12.0
 * django-rest-multiple-models==1.6.3
 * django-rest-swagger==0.3.5
 * djangorestframework==3.3.2
 * django-cors-headers==1.1.0
 * Markdown==2.6.5
 * mysqlclient==1.3.7
 * Pygments==2.1.1
 * PyYAML==3.11


### Docker support

Run Docker compose
```
sudo docker-compose up
```

###Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas (trakadasp)
 * Panos Karkazis (pkarkazis)

