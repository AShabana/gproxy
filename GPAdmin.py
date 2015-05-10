#!/usr/bin/python
from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from proxylib import counter
from proxylib import GPLists as showlist
from os import path, kill

# Showlist object

class YearPage(Resource):
	def __init__(self, year):
	#	Resource.__init__(self)
		self.year = year

	def render_GET(self, request):
		return "Processed from yearpage class"

class ShowCounters(Resource):
	isLeaf = True
	def render_GET(self, request):
		if filter(lambda x: x not in ('start', 'end' ,'link', 'month'), request.args.keys()):
			print "invalid request " , request.args
			return "Accepted args are start,end,link,month"
		smsc = request.args['link'][0] if request.args.has_key('link') else None
		start = request.args['start'][0] if request.args.has_key('start') else None
		end = request.args['end'][0] if request.args.has_key('end') else None
		month = request.args['month'][0] if request.args.has_key('month') else None
		c = counter.Collector(smsc=smsc, start=start, end=end, month=month)
		return str(c.count())

class ShowLists(Resource):  # should able to redirect to edit lists
	isLeaf = True
	def render_GET(self, request):
		sl = showlist.GPLists()
		print "fetch all lists"
		listall = request.args['listall'][0] if request.args.has_key('listall') else None
		res = sl.listall()
		return str(res)

class DisList(Resource):
	isLeaf = True
	def render_GET(self, request):
		sl = showlist.GPLists()
		if filter(lambda x: x not in 'list', request.args.keys()) or len(request.args.keys()) != 1:
			print 'invalid request ', request.args
			return 'Accepted args is list'
		listid = request.args['list'][0] if request.args.has_key('list') else None
		if listid == None :
				return " Could not find list : " + str(listid)
		res = sl.listlist(listid)
		return str(res)

class AddToList(Resource):
	isLeaf = True
	def render_GET(self, request):
		sl = showlist.GPLists()
		print "AddToList" , request.args
		if filter(lambda x: x not in ('sender', 'listid'), request.args.keys()) or len(request.args.keys()) != 2 :
			print 'invalid request ', request.args
			return 'Accepted args are sender , listid'
		sender = request.args['sender'][0] if request.args.has_key('sender') else None
		listid = request.args['listid'][0] if request.args.has_key('listid') else None
		res = sl.addtolist(sender,listid)
		return res

class DelFromList (Resource):
	isLeaf = True
	def render_GET(self, request):
		sl = showlist.GPLists()
		print "Remove from list" , request.args
		if filter(lambda x: x not in ('sender', 'sender_del', 'listid', 'listid_del'), request.args.keys()) or len(request.args.keys()) != 2:
			print 'invalid request ', request.args
			return 'Accepted args are sender , listid'
		sender_del = request.args['sender'][0] if request.args.has_key('sender') else request.args['sender_del'][0]
		listid_del = request.args['listid'][0] if request.args.has_key('listid') else request.args['listid_del'][0]
		res = sl.delfromlist(sender_del,listid_del)
		return res

class AddList(Resource):
		isLeaf = True 
		def render_GET(self, request):
			sl = showlist.GPLists()
			if filter(lambda x: x not in 'listid', request.args.keys()) or len(request.args.keys()) != 1:
				print 'invalid request ', request.args
				return 'Accepted arg listid'
			listid =  request.args['listid'][0] if request.args.has_key('listid') else None
			if listid == None :
					return 'listid arg not passed'
			else :
					print "Adding list " , listid
					return sl.addlist(listid)

class Restart(Resource):
		isLeaf = True
		def render_GET(self, request):
			with open('listener.pid', 'r') as f :
				p = f.read()
			kill(int(p), 1)
			print "Sending re-read config request to the listener."
			return "Done."

class GetListLength(Resource):
		isLeaf = True
		def render_GET(self ,request):
			if filter(lambda x: x not in ('listid',), request.args.keys()):
				print 'invalid request ', request.args
				return 'Accepted arg listid'
			listid =  request.args['listid'][0] if request.args.has_key('listid') else None
			if listid == None :
				return 'listid arg not passed'
			else :
				sl = showlist.GPLists()
				return str(len(sl.listlist(listid)))


class AppRoot(Resource):
	def getChild(self, name, request):
		if name == '':
			return self
		if name == 'ShowCounters':
			return ShowCounters()
		if name == 'ShowLists':
			return ShowLists()
		if name == 'DisList':
			return DisList()
		if name == 'AddToList':
			return AddToList()
		if name == 'DelFromList':
			return DelFromList()
		if name == 'AddList' :
			return AddList()
		if name == 'Restart' :
			return Restart()
		if name == 'GetListLength' :
			return GetListLength()
		else:
			txt = "Accepted Commands are: ShowCounters, ShowLists , DisList , AddToList , DelFromList , AddList, Restart, GetListLength"
			return NoResource(message=txt)

	def render_GET(self, request):
		return "calender class "
##T.D : make it callable from cmd and make this as a function (when run as main)
def web():
		root = AppRoot()
		factory = Site(root)
		print "Starting GPAdmin listening"
		reactor.listenTCP(3325, factory)
		reactor.run()

if __name__ == "__main__" :
		from sys import argv
		from os import system

		if len(argv) == 1 :
				web()
				exit(0)
		if argv[1] == "--web":
			web()
		elif argv[1] == "--counter":
			print "Loading Counter module"
			cmd = "python proxylib/counter.py "
			for i in argv[2:] :
					cmd = cmd + i + " " 
			print cmd
			system(cmd)
			exit(0)
		elif argv[1] == "--lists":
			print "Loading GPlists module"
			cmd = "python proxylib/GPLists.py "
			for i in argv[2:] :
					cmd = cmd + i + " " 
			print cmd
			system(cmd)
			exit(0)
		else :
			print "Unknown args "
			print "Accepted args are :"
			print "\t--web #To activate web interface"
			print "\t--counter #To Load counter admin module"
			print "\t--lists # To Load lists admin module"

