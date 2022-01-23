import os
import glob

import pandas as pd
import time as t
import sys
import datetime

from twisted.python import log
from twisted.internet.interfaces.IReactorUDP			//reactor connects protocol to UDP transport
from twisted.internet.protocol.DatagramProtocol			//class that receive datagrams
from twisted.internet import reactor, defer, threads 

import txthings.resource as resource
import txthings.coap as coap

import pigpio
from w1thermsensor import W1ThermSensor				//package for DS18B20

class tempSensor():
	
	def __init__(self, celsius):
		self.celsius = celsius
		self.sensor = W1ThermSensor()
		self.temperature = None
		reactor.callLater(0.1,self.read_temp_raw) 	
 
	def read_temp_raw(self):
	    	d=threads.deferToThread(self.sensor.get_temperature,W1ThermSensor.DEGREES_C)
 		d.addCallback(self.read_temp)

	def read_temp(self,result):
		self.temperature = result
		reactor.callLater(2,self.read_temp_raw)


class CounterResource (resource.CoAPResource):
	def __init__(self, start=0):
        	resource.CoAPResource.__init__(self)
        	self.counter = start
        	self.visible = True
        	self.addParam(resource.LinkParam("title", "Counter"))
  	def render_GET(self, request):
        	d = defer.Deferred()
        	reactor.callLater(3, self.responseReady, d, request)
        	return d
	def responseReady(self, d, request):
        	log.msg('response ready')
        	payload ="Welcome"
        	response = coap.Message(code=coap.CONTENT, payload=payload)
        	d.callback(response)
class TempResource (resource.CoAPResource):
	def __init__(self):
        	resource.CoAPResource.__init__(self)
        	self.visible = True
        	self.addParam(resource.LinkParam("title", "Temperature"))
        	self.sensor= TemperatureSensor(CELSIUS)
		self.notify()
	def notify(self):
        	log.msg('trying to send notifications')
        	self.updatedState()
        	reactor.callLater(1, self.notify)

    	def render_GET(self, request):
		result = self.sensor.temperature
		if result is not None:
			payload = ",".join(result)
			log.msg("%s",payload)
		      response = coap.Message(code=coap.CONTENT,
					 payload= payload)
       		response.opt.content_format
			=coap.media_types_rev['application/link-format']
        		
		else:
		  response=coap.Message(code=coap.SERVICE_UNAVAILABLE)
		  return defer.succeed(response)

log.startLogging(sys.stdout)
root = resource.CoAPResource()
def endpoint():
counter = CounterResource(5000)
node.putChild('counter',counter)
temperature = TempResource()
node.putChild('temperature', temperature)
endpoint = resource.Endpoint(root)
reactor.listenUDP(61616, coap.Coap(endpoint)) #, interface="::")
reactor.run()

while True:
        for int i in range(5):
                tm=read_temp()
                ts=t.time()
                df = df.append({'TS':ts, 'Temp':tm}, 				               ignore_index=True)
	print(df)
	df.to_csv('temp#.csv', index=False)
        print(read_temp())      
        time.sleep(1)
	
	

	









