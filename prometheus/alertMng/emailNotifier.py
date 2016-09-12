'''
Copyright (c) 2015 SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written 
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through 
the Horizon 2020 and 5G-PPP programmes. The authors would like to 
acknowledge the contributions of their colleagues of the SONATA 
partner consortium (www.sonata-nfv.eu).
'''

import smtplib, base64, os
import email.utils, re, json, urllib2
from email.mime.text import MIMEText


class emailNotifier():

    def __init__(self):
        self.user = 'monitoring@synelixis.com'
        self.psw = self.getEmailPass()
        self.mon_manager = 'http://manager:8000'
        self.msgs = []

    def getEmailPass(selfn):
        if os.environ.has_key('EMAIL_PASS'):
            key = str(os.environ['EMAIL_PASS']).strip()
            return key.decode('base64')
        else:
            return ''
            
    def msgs2send(self,msgs_):
        for notif in msgs_:
            myemail={}
            m = self.alarmStatus(notif)
            msg = MIMEText(m['body'])
            msg.set_unixfrom('Sonata Monitoring System')
            receivers = ['pkarkazis@synelixis.com']
            if notif['exported_job'] == 'vm': 
                msg['To'] = email.utils.formataddr(('Recipient', receivers))
            elif notif['exported_job'] == 'vnf':
                if 'UserID' in notif:
                    usr = self.getEmail(notif['UserID'])
                else:
                    usr={}
                    usr['email']='pkarkazis@synelixis.com'
                if 'email' in usr:
                    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', usr['email'])
                    if match == None:
                        continue
                    else:
                        if usr['email'] == 'system@system.com':
                            usr['email']='pkarkazis@synelixis.com'
                        receivers = [usr['email'],'trakadasp@yahoo.gr','jbonnet@alticelabs.com']
                        msg['To'] = email.utils.formataddr(('Recipient', usr['email']))
                else:
                    continue   
            msg['From'] = email.utils.formataddr(('Monitoring server', 'monitoring@synelixis.com'))
            msg['Subject'] = 'ALERT NOTIFICATION '+ m['status'] 
            myemail['receivers']= receivers
            myemail['obj'] = msg
            self.msgs.append(myemail)
            print(myemail['receivers'])
        self.sendMail()
            
    def getEmail(self, userid):
        try:
            url = self.mon_manager+'/api/v1/user/'+userid
            print url
            req = urllib2.Request(url)
            req.add_header('Content-Type','application/json')
        
            response=urllib2.urlopen(req, timeout = 3)
            code = response.code
            data = json.loads(response.read())
            return data
    
        except urllib2.HTTPError, e:
            return {'error':str(e)}
        except urllib2.URLError, e:
            return {'error':str(e)}
        except ValueError, e:
            return {'error':str(e)}
            
            
    def sendMail(self):
        if self.psw == '':
            return
        
        try:
            server = smtplib.SMTP('mail.synelixis.com',26)
            #server.set_debuglevel(1)
            server.ehlo()
            #server.starttls()
            #server.ehlo()
            server.login(self.user, self.psw)
            for msg in self.msgs:
                server.sendmail('monitoring@synelixis.com', msg['receivers'], msg['obj'].as_string())   
                print "Successfully sent email"
            server.quit()
        except Exception , exc:
            print "mail failed; %s" % str(exc)
            
    def alarmStatus(self, obj):
        msg={}
        msg['body'] = 'Dear user, \nRule: '
        alert = obj['alertname']
        if alert == 'CPU_load_vm':
            alert = alert + ' ('+obj['core']+')'
        if obj['alertstate'] == 'firing' and obj['value'] == "1":
            msg['body'] = msg['body'] + alert + " is ACTIVE on instance "+obj['id'] + " at " + obj['time']+'\n\n'+json.dumps(obj)
            msg['status'] = "ACTIVE!!"
            
            return msg
        elif obj['alertstate'] == 'firing' and obj['value'] == "0":
            msg['body'] = msg['body'] + alert + " is DEACTIVATED on instance "+obj['id'] + " at "+ obj['time'] +'\n\n'+json.dumps(obj)
            msg['status'] = "DEACTIVATED!!"
            return msg
        elif obj['alertstate'] == 'pending' and obj['value'] == "0":
            msg['body'] = msg['body']+ alert+ " is ACTIVATED!! on instance "+obj['id'] + " at "+ obj['time'] +'\n\n'+json.dumps(obj)
            msg['status'] = "ACTIVATED!!"
            return msg
