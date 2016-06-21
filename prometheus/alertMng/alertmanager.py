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

def checkServPlatform(time_window):
    global count
    cl = influx('influx',8086,'','','prometheus')
    #resp = cl.databases()
    #print resp
    #resp = cl.getseries()
    #print resp
    
    resp = cl.query('select * from ALERTS where alertstate=\'firing\' and value=1 and time > now() - '+ time_window)
    if 'series' in resp:
        print 'Active Alerts'
        for serie in resp['series']:
            for rec in serie['values']:
                pool.addQueueMsg(rec,serie['columns'])
        
    
    resp = cl.query('select * from ALERTS where alertstate=\'pending\' and value=0 and time > now() - '+ time_window)
    if 'series' in resp:
        print 'Event Started'
        for serie in resp['series']:
            for rec in serie['values']:
                pool.addEmailMsg(rec,serie['columns'])
                pool.addSmsMsg(rec,serie['columns'])
                print(rec)
    
    resp = cl.query('select * from ALERTS where alertstate=\'firing\' and value=0 and time > now() - '+ time_window)
    if 'series' in resp:
        print 'Event Stoped'
        for serie in resp['series']:
            for rec in serie['values']:
                pool.addEmailMsg(rec,serie['columns'])
                pool.addSmsMsg(rec,serie['columns'])
        
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
    try:
        rabbit = getRabbitUrl()
        if rabbit == '':
            raise ValueError('Rabbimq url unset') 
        host = rabbit.split(':')[0]
        port = int(rabbit.split(':')[1])
    except ValueError as err:
        print(err.args)
        return

    while 1:
        if len(pool_) > 0:
            if rabbit == '':
                return
            rmq=amqp(host,port, 'son.monitoring', 'guest', 'guest')
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
    
    print(time.ctime() + getEmailPass() + getRabbitUrl())
    checkServPlatform('15s')    
    threading.Timer(7, checkAlerts).start()
