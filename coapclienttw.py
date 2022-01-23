import sys
from ipaddress import ip_address

from twisted.internet import reactor
from twisted.internet.defer import deferred
from twisted.internet.protocol import protocol
from twisted.web.client import agent
from twisted.python import log

import txthings.coap as coap
import txthings.resource as resource
import time 

class coapProtocol:
	
	def __init__(self, protocol):
        	self.protocol = protocol
        	reactor.callLater(0.1, self.requestResource)
	def requestResource(self):
        	request = coap.Message(code=coap.GET)
		request.opt.uri_path = (b'test',)         	request.opt.observe = 0
        	request.remote = (ip_address("192.168.43.61"), coap.COAP_PORT)
        def printResponse(self, response):
        	log.msg(response)
		t2=time.time()
		self.transpot.write(response.payload,'utf-8')
        	log.msg("First result: " + str(response.payload, 'utf-8'))
	def noResponse(self, failure):
        	log.msg("Failed to fetch resource")

agent = Agent(protocol)
t1= time.time()
log.startLogging(sys.stdout)
log.msg("Welcome Home")
log.msg("Retriving home data")
d = agent.requestResource(self)
d.addCallback(self.printResponse)
d.addErrback(self.noResponse)
endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
reactor.listenUDP(61616, protocol)  # , interface="::")
t2=time.time()
t3= str(t2-t1)
print("UDP transmission time:"+t3)
reactor.run()
