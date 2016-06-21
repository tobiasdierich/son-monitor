# To change this template file, choose Tools | Templates
# and open the template in the editor.

from influxdb import InfluxDBClient
import json

class influx(object):
    def __init__(self, host, port, usr, psw, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = usr
        self.password = psw
        
    def query(self, query_):
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.db_name)
        result = client.query(query_)
        return result.raw
    
    def databases(self):
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.db_name)
        result = client.get_list_database()
        return result
    
    def getseries(self):
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.db_name)
        result = client.get_list_series(self.db_name)
        return result
