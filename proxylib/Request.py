from twisted.web.client import reactor as creact, getPage
from twisted.python import log
from cStringIO import StringIO
import urllib2
import urllib
from twisted.python.util import println
import random
import string
import re

class requestObject(object):

	def __init__(self, request):
		self.req = request
	def send(self):
		url  = 	"".join(("http://" , self.req['Kannel-host']\
								,":", self.req['Kannel-port']\
								,"/cgi-bin/sendsms?smsc="\
								,self.req['smsc']\
								,"&account=" , self.req['account']\
								,"&limit=" , self.req['limit']\
								,"&udh=" , urllib2.quote(self.req['udh'])\
								,"&from=", urllib2.quote(self.req['from'])\
								,"&to=" , self.req['to']\
								,"&text=", urllib.quote(self.req['text'])\
								,"&coding=", self.req['coding']\
								,"&dlr-mask=", self.req['dlr-mask']\
								,"&dlr-url=", urllib2.quote(self.req['dlr-url'])))
		getPage(url).addCallbacks(callback=lambda value:(println(value)),errback=lambda error:(println("an error occurred : ", url) )) 
		COUNTER(self.req['smsc'], self.req['text'], self.req['coding'])
	
	def getRandomSenderFromPrefix(self, prfx):
		return "%d%d" % (int(prfx),random.randrange(0, 10000000000, 10))

	def getRandomSender(self):
		return self.getRandomSenderFromPrefix("234")
	
	def alfaSender(self, length=6, chars=string.ascii_lowercase ):
		if self.req.has_key("udh") :
			if self.req["udh"] is not None  and len(self.req["udh"]) > 1 :
				x=self.req["udh"]
				return "O%s" % ( (re.sub('%', '', urllib2.quote(x)))[0:-2] )
		if chars == 'C': chars = string.ascii_uppercase
		if chars == 'S': chars =string.ascii_lowercase
		if chars in ('S+C' ,'C+S'): chars =  string.ascii_lowercase + string.ascii_uppercase
		if chars in ('S+D' ,'D+S'): chars = string.ascii_lowercase + string.digits
		if chars in ('C+D' ,'D+C'): string.ascii_uppercase + string.digits
		if chars in ('S+D+C', 'S+C+D', 'C+S+D', 'C+D+S', 'D+S+C', 'D+C+S'): chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
	        return ''.join(random.choice(chars) for _ in range(length))


	@property
	def kannelIP(self):
		return self.req['Kannel-host']
	@kannelIP.setter
	def kannelIP(self, x): ###
		log.msg("\tChanging kannel ip from  : %s to : %s " % (self.req['Kannel-host'],x))
		self.req['Kannel-host'] = x
	
	@property
	def kannelPort(self):
		return self.req['Kannel-port']
	@kannelPort.setter
	def kannelPort(self, x): ###
		log.msg("\tChanging kannel Port from %s to %s " % (self.req['Kannel-port'],x))
		self.req['Kannel-port'] = x

	@property
	def smsc(self):
		return self.req['smsc']
	@smsc.setter
	def smsc(self, x):
		log.msg( "\tChanging smsc from  : %s to : %s " % (self.req['smsc'],x))
		self.req['smsc'] = x
	
	@property
	def account(self):
		return self.req['account']
	@account.setter
	def account(self, x):
		log.msg("\tChanging account from  : %s to : %s " % (self.req['account'],x))
		self.req['account'] = x


	@property
	def limit(self):
		return self.req['limit']
	@limit.setter
	def limit(self,x):
		log.msg("\tChanging limit from  : %s to : %s " % (self.req['limit'],x))
		self.req['limit'] = x

	@property
	def udh(self):
		return self.req['udh']
	@udh.setter
	def udh(self,x):
		log.msg("\tChanging UDH from  : %s to : %s " % (self.req['udh'],x))
		self.req['udh'] = x

	@property
	def sender(self):
		return self.req['from']
	@sender.setter
	def sender(self,x):
		log.msg( "\tChanging Sender from  : %s to : %s " % (self.req['from'],x) )
		self.req['from'] = x
		pass

	@property
	def to(self):
		return self.req['to']
	@to.setter
	def to(self,x):
		log.msg("\tChanging destination from  : %s to : %s " % (self.req['to'],x))
		self.req['to'] = x

	@property
	def msg(self):
		return self.req['text']
	@msg.setter
	def msg(self,x):
		log.msg("\tChanging msg from  : %s to : %s " % (self.req['text'],x))
		self.req['msg'] = x

	@property
	def coding(self):
		return self.req['coding']
	@coding.setter
	def coding(self,x):
		log.msg("\tChanging coding from  : %s to : %s " % (self.req['coding'],x))
		self.req['coding'] = x

	@property
	def dlrMask(self):
		return self.req['dlr-mask']
	@dlrMask.setter
	def dlrMask(self,x):
		log.msg("\tChanging DLR-MASK from  : %s to : %s " % (self.req['dlr-mask'],x))
		self.req['dlr-mask'] = x

	@property
	def dlrURL(self):
		return self.req['dlr-url'] 
	@dlrURL.setter
	def dlrURL(self,x):
		log.msg("\tChanging DLR-URL from  : %s \nto : %s " % (self.req['dlr-url'],x))
		self.req['dlr-url'] = x




if __name__ == "__main__" :
	req = { 'Kannel' : {
						 'host':'localhost',
						 'port': 8000,
						 'user': 'Nemra1',
						 'pass' : 'koko88'
				   },
		 'account' : 'Ehab',
		 'limit': '',
		 'udh' : '',
		 'smsc' : 'link1',
		 'from' : 'SNDR!',
		 'to' : '',
		 'text' : '',
		 'coding' : '',
		 'dlr-mask' : 7,
		 'dlr-url' : ''

   }


	incomingRequest = requestObject(req)
	print "Before Editing"
	print "%s" % incomingRequest.sender
	incomingRequest.sender = "HAMDA"
	print "After Editing "
	print incomingRequest.sender
	print incomingRequest.req['from']
	print "DLR MASK %s" % incomingRequest.dlrMask
	print incomingRequest.getRandomSender()
	print incomingRequest.getRandomSenderFromPrefix(12345)
	
