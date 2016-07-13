# son-monitor [![Build Status](http://jenkins.sonata-nfv.eu/buildStatus/icon?job=son-monitor)](http://jenkins.sonata-nfv.eu/job/son-monitor)
Sonata's monitoring system gathers, analyzes performance information from NS/VNF and provides alarm notifications, based on alarm definitions which have been defined from the users. The architecture of the system is based on data exporters and a monitoring server. Data exporters sends monitoring data from NS/VNFs to monitoring server which collects, analyses, stores data and generates the appropriate notifications. In generally monitoring server consisting of a rest api interface, an alerting mechanism (based on prometheus.io), a timeseries DB and a real time notification service.

### Dependencies
 * docker-compose==1.6.2 (Apache 2.0)
 * Django==1.9.2 (BSD)
 * django-filter==0.12.0 (BSD)
 * django-rest-multiple-models==1.6.3 (MIT)
 * django-rest-swagger==0.3.5 (BSD)
 * djangorestframework==3.3.2 (BSD)
 * django-cors-headers==1.1.0 (MIT)
 * Markdown==2.6.5 (BSD)
 * Pygments==2.1.1 (BSD)
 * PyYAML==3.11 (MIT)
 * Prometheus==0.17 (Apache 2.0)
 * Pushgateway==0.2.0 (Apache 2.0)


### Installation

Run Docker compose
```
sudo docker-compose up
```
### License
SONATA gui is published under Apache 2.0 license. Please see the LICENSE file for more details.

###Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.
 
 * Panos Trakadas (trakadasp)
 * Panos Karkazis (pkarkazis)

#### Feedback-Chanel
* You may use the mailing list sonata-dev@lists.atosresearch.eu
* Please use the GitHub issues to report bugs.