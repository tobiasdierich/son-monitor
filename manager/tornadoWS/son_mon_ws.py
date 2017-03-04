# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import uuid
import json
import tornado.ioloop
import tornado.web
from tornado import websocket
from collector import PushGW

class NameSpaceHandler(object):
    
    def __init__(self):
        self.client_info = {}  
        self.nm_space_info = {}  
                
        
    def add_name_space(self, metric, params):
        #Add namespace. Return generated ID
        cid = uuid.uuid4().hex  # generate a client id.
        if not metric in self.nm_space_info:  
            self.nm_space_info[metric] = []
        
        self.client_info[cid] = {'metric_name': metric, 'filters': params}  
        self.nm_space_info[metric].append({'cid': cid, 'filters': params})
        return cid
    
    def add_nmspace_wsconn(self, client_id, conn):
        #Store the websocket connection corresponding to an existing client.
        self.client_info[client_id]['wsconn'] = conn
        cid_room = self.client_info[client_id]['metric_name']

        for user in self.nm_space_info[cid_room]:
            if user['cid'] == client_id:
                user['wsconn'] = conn
                break

    def remove_nmspace_wsconn(self, client_id):
        del(self.client_info[client_id])
       
class ClientWSConnection(websocket.WebSocketHandler):

    def initialize(self, ws_hdl):
        self.__rh = ws_hdl
        
    def check_origin(self, origin):
        return True

    def open(self, client_id):
        self.__clientID = client_id
        self.__rh.add_nmspace_wsconn(client_id, self)
        print "WebSocket opened. ClientID = %s" % self.__clientID
        print(self.__rh.nm_space_info)
        print(self.__rh.client_info)
        response = {'Status': 'Socket Opened'}
        self.send_values(response)

    def on_message(self, message):
        response = {'Error': 'Current version doesnt support incomming messages'}
        self.send_values(response)
        
            
    def send_values(self, message):
        self.write_message(message)

    def on_close(self):
        print "WebSocket closed"
        self.__rh.remove_nmspace_wsconn(self.__clientID)

class MainHandler(tornado.web.RequestHandler):

    def initialize(self, ws_hdl):
        self.__rh = ws_hdl

    def get(self):
        try:
            metric = self.get_argument("metric")
            params= self.get_argument("params")
    
            cid = self.__rh.add_name_space(metric, params)
            print 'cid: ' + cid + ' parameters: '+params
            
            response = {'name_space': cid}
            self.write(response)
        except tornado.web.MissingArgumentError:
            response = {'Error': 'Missing Argument'}
            self.write(response)
            


if __name__ == "__main__":
    hld = NameSpaceHandler()
    pw = PushGW('http://sp.int3.sonata-nfv.eu:9091/metrics',hld)
    
    app = tornado.web.Application([
        (r"/new/", MainHandler, {'ws_hdl': hld}),
        (r"/ws/(.*)", ClientWSConnection, {'ws_hdl': hld})
        ],
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )
    app.listen(8888)
    print 'Monitoring WS service started.'
    print 'listening on 8888 ...'
    tornado.ioloop.IOLoop.instance().start()
