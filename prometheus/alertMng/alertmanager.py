# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from influxDB import influx
from msg_pools import msgs
import json, os, base64
import time, threading, urllib2
from threading import  Thread 
from rabbitMQ import amqp
from emailNotifier import emailNotifier  


__author__="panos"
__date__ ="$May 31, 2016 6:46:27 PM$"
#msgs = [{"exported_instance": "INT-SRV-1", "core": "cpu0", "group": "development", "exported_job": "vm", "ruleID": "58", "userID": "22", "last_notif": "null", "value": "1", "instance": "pushgateway:9091", "job": "sonata", "serviceID": "005606ed-be7d-4ce3-983c-847039e3a5a3", "alertname": "CPU_load_vm", "time": "2016-06-02T08:17:07.808Z", "alertstate": "firing", "id": "c4ef3f60-3d9a-4c8a-95ee-a665bf2cf483", "monitor": "sonata-monitor"]
#mailNotf = emailNotifier()
#mailNotf.msgs2send(msgs)

def checkServPlatform(time_window):
    global count
    cl = influx('influx',8087,'','','prometheus')
    #resp = cl.databases()
    #print resp
    #resp = cl.getseries()
    #print resp
    
    resp = cl.query('select * from ALERTS where exported_job=\'vm\' and alertstate=\'firing\' and value=1 and time > now() - '+ time_window)
    if 'series' in resp:
        print 'Active Alerts'
        for serie in resp['series']:
            for rec in serie['values']:
                #print 'time: '+rec[0]+' alertname: '+ rec[1]+' core: '+ rec[3]+ ' alertstate: '+ rec[2] +' value: '+ str(rec[14])
                pool.addQueueMsg(rec,serie['columns'])
        #print resp['series'][0]['values']. json.dumps(resp['series'])
    #else:
    #    print "NO ACTIVE ALERTS"
        
    
    resp = cl.query('select * from ALERTS where exported_job=\'vm\' and alertstate=\'pending\' and value=0 and time > now() - '+ time_window)
    if 'series' in resp:
        print 'Event Started'
        for serie in resp['series']:
            for rec in serie['values']:
                pool.addEmailMsg(rec,serie['columns'])
                pool.addSmsMsg(rec,serie['columns'])
                print 'time: '+rec[0]+' alertname: '+ rec[1]+' core: '+ rec[3]+ ' alertstate: '+ rec[2] +' value: '+ str(rec[14])
    #else:
    #    print "NO START EVENT"
    
    resp = cl.query('select * from ALERTS where exported_job=\'vm\' and alertstate=\'firing\' and value=0 and time > now() - '+ time_window)
    if 'series' in resp:
        print 'Event Stoped'
        for serie in resp['series']:
            for rec in serie['values']:
                pool.addEmailMsg(rec,serie['columns'])
                pool.addSmsMsg(rec,serie['columns'])
                #print 'time: '+rec[0]+' alertname: '+ rec[1]+' core: '+ rec[3]+ ' alertstate: '+ rec[2] +' value: '+ str(rec[14])
    #else:
    #    print "NO END ALERT"
        
def checkAlerts():
    print(time.ctime())
    checkServPlatform('15s')
    threading.Timer(10, checkAlerts).start()


def emailConsumer(pool_):
    while 1:
        if len(pool_) > 0:
            
            mailNotf = emailNotifier()
            msgs = pool_
            print 'send mails : ' + json.dumps(msgs) +' number of mails: '+ "".join(str(len(msgs)))
            mailNotf.msgs2send(msgs)
            del pool_[:]
            #msg = pool_[0]
            #del pool_[0]
        time.sleep(4)
        
def smsConsumer(pool_):
    vm_dt = ''
    while 1:
        if len(pool_) > 0:
            msg = pool_[0]
            del pool_[0]
            print 'send sms : ' + json.dumps(msg) +' remain: '+ "".join(str(len(pool_)))
        time.sleep(0.2)
        
def rabbitConsumer(pool_):
    rabbit = getRabbitUrl()
    host = rabbit.split(':')[0]
    port = int(rabbit.split(':')[1])
    print rabbit
    while 1:
        if len(pool_) > 0:
            if rabbit == '':
                return
            rmq=amqp(host,port, 'Monitoring', 'user', 'user')
            #rmq=amqp('192.168.1.39',5672, 'Monitoring', 'user', 'user')
            msg = pool_[0]
            rmq.send(json.dumps(msg))
            del pool_[0]
            print 'send rabbitmq : ' + json.dumps(msg) +' remain: '+ "".join(str(len(pool_)))
        time.sleep(0.2)
        

def getRabbitUrl():
    if os.environ.has_key('RABBIT_URL'):
        return str(os.environ['RABBIT_URL']).strip()
    else:
        return ''

def getEmailPass():
    if os.environ.has_key('EMAIL_PASS'):
        key = str(os.environ['EMAIL_PASS']).strip()
        return key.decode('base64')
    else:
        return ''


if __name__ == "__main__":
    global pool
    
    count = 0
    pool = msgs()
    t1 = Thread(target = emailConsumer, args=(pool.getEmailMsgs(),))
    t2 = Thread(target = smsConsumer, args=(pool.getSmsMsgs(),))
    t3 = Thread(target = rabbitConsumer, args=(pool.getQueueMsgs(),))
    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t1.start()
    t2.start()
    t3.start()
    
    print(time.ctime() + getEmailPass())
    checkServPlatform('15s')    
    threading.Timer(7, checkAlerts).start()    


