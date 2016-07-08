# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import json

class msgs(object):
    email=[]
    sms=[]
    queue=[]
    
    def init(self):
        self.sms=[]
        self.email=[]
        self.queue=[]

    
    def addQueueMsg(self,obj,columns):
        self.queue.append(self.list2obj(obj,columns))
    
    def addEmailMsg(self,obj,columns):
        self.email.append(self.list2obj(obj,columns))
         
    def addSmsMsg(self,obj,columns):
        self.sms.append(self.list2obj(obj,columns))
        
    def getQueueMsgs(self):
        return self.queue
    
    def getEmailMsgs(self):
        return self.email
    
    def getSmsMsgs(self):
        return self.sms
    
    def list2obj(self,el,columns):
        msg = '{'
        index = 0
        for col_name in columns:
            msg=msg+'\"'+col_name+'\" :\"'+str(el[index])+'\",'
            index += 1
        msg=msg[:-1]+'}'
        obj = json.loads(msg)
        return obj
         
