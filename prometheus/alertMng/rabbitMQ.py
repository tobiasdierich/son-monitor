# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import pika

__author__="panos"
__date__ ="$Nov 24, 2015 3:08:24 PM$"

if __name__ == "__main__":
    print "Hello RMQ"


class amqp(object):
    def __init__(self, host, port, queue, usr, usr_pass):
        self.host = host
        self.port = port
        self.queue = queue
        self.user = usr
        self.password = usr_pass
        
    def send(self, msg):
        credentials = pika.PlainCredentials(self.user, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host ,self.port,'/',credentials))
        channel = connection.channel()

        channel.queue_declare(queue = self.queue)

        channel.basic_publish(exchange='',routing_key=self.queue, body=msg)
        connection.close()
