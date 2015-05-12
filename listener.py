from twisted.web import server, resource
from runtime import *
from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.python.util import println
from twisted.web.client import reactor as creact, getPage
import configobj
import uuid
import urllib
import urllib2
import signal
import time
from sys import stdout, argv
from os import getpid
from proxylib import Request, counter, GPLists
import __builtin__
import imp
import signal
import configobj
import getopt

class KannelProxy(resource.Resource):
	isLeaf = True
	class bcolors:
			HEADER = '\033[95m'
			OKBLUE = '\033[94m'
			OKGREEN = '\033[92m'
			WARNING = '\033[93m'
			FAIL = '\033[91m'
			ENDC = '\033[0m'

	def __init__(self):
		log.msg("Starting the gproxy inist")
	
	def loadConfig(self,path=None):
		gplists = GPLists.GPLists(path)
		return gplists.load()

	def verifyURL(self, url):
		IncomingRequest={}
		try:
			#url.setHeader("content-type", "text/plain")
			IncomingRequest['Kannel-host'] = "ksa"
			IncomingRequest['Kannel-port'] = "8007"
			#url.args['Kannel']['user']
			IncomingRequest['account'] = url.args['account'][0] if url.args.has_key('account') else ""
			IncomingRequest['limit'] = url.args['limit'][0] if url.args.has_key('limit') else ""
			IncomingRequest['udh'] = url.args['udh'][0] if url.args.has_key('udh') else ""
			IncomingRequest['smsc'] = url.args['smsc'][0][8:]
			IncomingRequest['from'] = url.args['from'][0]
			IncomingRequest['to'] = url.args['to'][0]
			IncomingRequest['text'] = url.args['text'][0]
			IncomingRequest['coding'] = url.args['coding'][0] if url.args.has_key('coding') else ""
			IncomingRequest['dlr-mask'] = url.args['dlr-mask'][0] if url.args.has_key('dlr-mask') else ""
			IncomingRequest['dlr-url'] = url.args['dlr-url'][0] if url.args.has_key('dlr-url') else ""
			return IncomingRequest
		except NameError, e :
			log.err("bad request error and print the request .") ###
			log.err(e.message)
			return -1
	
	def render_GET(self, url):
		request = self.verifyURL(url)
		if request == -1 :
			return "Not Ok."
		try :
			log.msg(self.bcolors.OKBLUE + "\"\"\"Executing scenario %s\"\"\"" % request['smsc'] + self.bcolors.ENDC)
			url.setResponseCode(200)
			scenario = globals()[request['smsc']]
			scenario.exe(request)
			return "Ok."
		except KeyError :
			log.msg("Error : Could not find scenario for  %s" % request['smsc'])
			return "Ok."
			
def signal_handler(sig, stack):
	if sig == signal.SIGHUP :
		print "[listener->pid:%d]: Received SIGHUP" %(getpid())
		print "[listener->pid:%d]: Reload the configuration" %(getpid())
		loadConfiguration(app, path)
		print "[listener->pid:%d]: Release open fds. ToDo" %(getpid())

def loadConfiguration(app, path):
	__builtin__.Config = {}
	__builtin__.Config = app.loadConfig(path)

def main(argv):
	""" Usage python listener.py -f path/to/conf-file or python listener.py"""
	try :
		opts, args = getopt.getopt(argv, "f:h", ["config-file","help"])
	except getopt.GetoptError:
		print main.__doc__
		exit(1)
	if len(opts) == 0 :
		CONF = configobj.ConfigObj("config/app.conf")
	else :
		for opt,arg in opts:
			if opt in ("-f", "--config-file"):
				CONF = configobj.ConfigObj(arg)
	print "configs are :"
	print CONF
	__builtin__.app = globals()[CONF['logic']]() 
	print "write pid to file -> %s" %(CONF['pid-file'])
	with open(CONF['pid-file'],"wb") as fd :
		fd.write("%d" % getpid())
	print "[listener->pid:%d]: app lunched " %(getpid())
	print "[listener->pid:%d]: depoloying signals handler" %(getpid())
	signal.signal(signal.SIGHUP, signal_handler)
	signal.signal(signal.SIGUSR1, signal_handler)
	print "[listener->pid:%d]: load configs" %(getpid())
	loadConfiguration(app, CONF['lists'])
	_file = CONF['log-file']
	print "[listener->pid:%d]: load counters "  %(getpid())
	c = counter.Counter(CONF['counter-path'])
	__builtin__.COUNTER = c.increment
	print "[listener->pid:%d]: Register logger to the app" % (getpid())
	print "[listener->pid:%d]: Registering app to the listeners .." %(getpid())
	for port in CONF['ports'].split(','): # 2 ranges odd and even
		reactor.listenTCP(int(port), server.Site(app))
		print "[listener->pid:%d]:\tport:%d" %(getpid(), int(port))
	print "[listener->pid:%d] deploy logger at file %s" %(getpid(), _file) 
	#__builtin__.log = 
	log.startLogging(DailyLogFile.fromFullPath(_file))
	log.msg("[listener->pid:%d]: starting .." % (getpid(),))
	reactor.run()

if __name__ == "__main__":
	main(argv[1:])
