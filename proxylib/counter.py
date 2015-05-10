from os import path, chdir, listdir, remove, getpid
import marshal
import sys ,getopt
import shutil
import glob, re
import datetime
from datetime import datetime as dt
import marshal

class Counter(object):
	def __init__(self, dirName):
		"""
		x. load from counter presistance dir today counters and put it at shm
		x. load shm all today counters then delete them
		"""
		self.c = {}
		if not path.exists('./' + dirName):
			print("no runtime coutner path found!!"  )	
			exit(11)
		self._shm_seg = "/dev/shm/gproxy/" + dirName + "/"
		if not path.exists(self._shm_seg):
			print("shm not exist " + self._shm_seg)
			exit(12)

	def printCounters(self,link='all'):
		if link == 'all':
			print self.c
		elif c.has_key(link):
			print c[link]
		else:
			print "%s have no couters !!" %(link,)

	def presistCoutner(self):
		""" Copy from shm to presist , append all pid/day/link counter to one """
		pass

	def _counters2shm(self):
		for link in self.c :
			f = self._shm_seg + str(getpid()) + dt.now().strftime(".%d.%m.%Y.") + link
			with open(f, 'w+') as fd :
				marshal.dump(self.c[link], fd)

	def increment(self, link, msg, encoding):
		c = self.c
		if not c.has_key(link): 
			c[link] = {}
			c[link]['parts'] = 0
			c[link]['submits'] = 0
		c[link]['parts'] += self._calcParts(msg, encoding )
		c[link]['submits'] += 1
		self._counters2shm()
		#print c


	def _calcParts(self, msg, encoding):
		if int(encoding) == 2 :
			length = len(msg)/2
			coding = 2
		elif int(encoding) == 0 :
			length = len(msg)
			coding = 0
		if coding == 0 :
			if length in range(1,161):
				return 1
			elif length in range(160,321):
				return 2
			elif length in range(320,481):
				return 3
			elif length in range(480,641):
				return 4
			elif length in range(640,801):
				return 5
			elif length in range(800,961):
				return 6
			elif length in range(960,1121):
				return 7
			elif length in range(1120,1281):
				return 8
		elif coding == 2:
			if length in range(0*140, 1*140+1) :
				return 1	
			if length in range(1*140, 2*140+1) :
				return 2	
			if length in range(2*140, 3*140+1) :
				return 3	
			if length in range(3*140, 4*140+1) :
				return 4	
			if length in range(4*140, 5*140+1) :
				return 5	
			if length in range(5*140, 6*140+1) :
				return 6	
			if length in range(6*140, 7*140+1) :
				return 7	
			if length in range(7*140, 8*140+1) :
				return 8	
		return 0



"""
This script just will parse passed files to it **it will NOT know anything regard date**

# This should contains 2 parts
# part 1 concern all files at /dev/shm/gproxy that is not today
# part 2 concern all files that not related to the running pids

other script will case about date and time margine i.e. count --smsc=linkX --start-date
before_today_counters=$(find /dev/shm/gproxy/counters -mtime +1 )
for file in before_today_counters
do
	python collect_coutner.py file
done 
"""

class Collector: # May modified to be __iteratable__
	def __init__(self, smsc=None, month=None, start=None, end=None, DEBUG=False):
		self._DEBUG = DEBUG
		self.counters = {} 
		self._SHM_SEG_ = "/dev/shm/gproxy/counters/"
		self._PRST_STRG_ =  "./counters/"
		self.__counters_files = []
		print "link:%s-month:%s-start:%s-end:%s" % (smsc, month, start, end) if DEBUG else ""
		self.__collect_counters_files(smsc, month, start, end)

	def dump(self): # TODO get size and policies count
		print "Memory Data :" ,self._SHM_SEG_
		print "Coutners : " ,self._PRST_STRG_
		return self._SHM_SEG_, self._PRST_STRG_

	class CollectorException(RuntimeError):
		def __init__(self, string, ErrorCode): # Edit it to handle ErrorCodes
			print string

	class CounterMetaData(object):
		def __init__(self, file_name ,_checker_callback): 
			""" The callback only to remove duplicated implementation for __chk_counter_metaData()without using inhertance """
			self.pid, self.day, self.month, self.year = _checker_callback(file_name)[0]
			self.smsc = _checker_callback(file_name)[1]
		def getPID(self):
			return self.pid
		def getDay(self):
			return self.day
		def getMonth(self):
			return self.month
		def getYear(self):
			return self.year
		def getSMSC(self):
			return self.smsc

	def __collect_counters_files(self, smsc=None, month=None, start=None, end=None): #TODO : Re-write this to be more unified and set self._start, self._end
		"""
		This contain the logic of collecting files from run time folder or presistent folder
		This is just concerns **edit** self.__counters_files
		"""
		if None not in (smsc, month) :
			print "Collecting  counters for link %s in month %s" % (smsc, month )
			files = glob.glob("%s/*.%s" % (self._PRST_STRG_, smsc)) # Extract smsc counter
			for f in files: 
				try:
					cMData = self.CounterMetaData(f, self.__chk_counter_metaData)
					if int(month) == int(cMData.month):
						self.__counters_files.append(f)
				except:
					continue 

		elif None not in (smsc, start, end):
			print "Collecting counters for link (%s) between %s and %s" %(smsc, start, end)
			startDate = dt.strptime(start, "%d%m%Y").date()
			endDate   = dt.strptime(end  , "%d%m%Y").date()
			files = glob.glob("%s/*.%s" % (self._PRST_STRG_, smsc))
			self.__iterate_files_between_dates(files, startDate, endDate)
		
		elif None not in (start, end):
			print "Collecting all counters in time between %s and %s" %(start, end)
			startDate = dt.strptime(start, "%d%m%Y").date()
			endDate   = dt.strptime(end  , "%d%m%Y").date()
			files = map(lambda f: "{0}/{1}".format(self._PRST_STRG_,f), listdir(self._PRST_STRG_))
			self.__iterate_files_between_dates(files, startDate, endDate)

		elif start is not None:
			print "Collecting all counters from date: %s to %s **yesterday**" %(start,datetime.timedelta(days=1))
                        startDate = dt.strptime(start, "%d%m%Y")
			endDate =  dt.now() - datetime.timedelta(days=1)
			files = map(lambda f: "{0}/{1}".format(self._PRST_STRG_,f), listdir(self._PRST_STRG_))
			self.__iterate_files_between_dates(files, startDate, endDate)

		elif smsc is not None:
			print "Collecting all counters for smsc %s" % (smsc,)
			self.__counters_files = glob.glob("%s*.%s" % (self._PRST_STRG_, smsc))
		elif month is not None:
			print "Collecting all counters for month %s" %(month,)
			startDate = dt.strptime("01%s%s"%(month,dt.now().year), "%d%m%Y").date()
			endDate = self.__increment_one_month(startDate)
			files = map(lambda f: "{0}/{1}".format(self._PRST_STRG_,f), listdir(self._PRST_STRG_))
			##@DEBUG print files
			self.__iterate_files_between_dates(files, startDate, endDate)
		else:
			print "Initialize collector by -> collecting today counters"
			self.__counters_files = listdir(self._SHM_SEG_)
			self.__counters_files = map(lambda f: "{0}/{1}".format(self._SHM_SEG_,f), listdir(self._SHM_SEG_))
		#@DEBUG 
		#print self.__counters_files 

	def __increment_one_month(self, sourcedate):
		month = sourcedate.month + 1
		year =  sourcedate.year + month/12
		if year == int(sourcedate.year) + 1:
			month = 1
		day = 1
		return datetime.date(year,month,day)

	def __counter_datestamp(self, file_name):
		cMData = self.CounterMetaData(file_name, self.__chk_counter_metaData)
		return dt.strptime("{0}{1}{2}".format(cMData.getDay(), cMData.getMonth(), cMData.getYear()) , "%d%m%Y").date()
	
	def __iterate_files_between_dates(self, files_list, startDate, endDate): # TODO: Check startDate < endDate
		for f in files_list:
			try:
				counterDate = self.__counter_datestamp(f)
				##DEBUG
				#print counterDate 
				#print "Start Date",startDate
				#print "End Date" ,endDate
				##DEBUG
			except:
				continue

			if startDate <= counterDate and  counterDate < endDate:
				self.__counters_files.append(f)
				#print "file %s within range"%(f,) ##@DEBUG
	
	def presist(self):
		""" 
		This removes counters from shm to presistence folder 
		this take in consideration those facts :
			- file names in this form PID.DAY.MONTH.YEAR.SMSC
			- copying a file for a running PID from the shm to presistence storage should not cause any issue even if this file exist before **it will replace old**
			- to avoid shm from taking so much space we MUST remove files that is not belongs to any running proxy PID (!) ,removing a file for a running process will cause counter invalid data (as it will replace the moved one) 
			- from previous point we must check access time ** os.path.getmtime(file) **
		"""
		pass

	def count(self):
		""" Iterator of Counter Class just iterates for self.__counters_files and update self.counters """
		for FILENAME in self.__counters_files:
			self.__load_counter(FILENAME)
		#print self.counters  ##@DEBUG
		#self.printCounters('DAILY', 'UNIXFILE')
		return self.counters
	
	def countPerDay(self): # TODO: use __counter_datestamp
		pass

	def countPerSMSC(self):	# TODO
		pass

	def printCounters(self, Format='daily', protocol='unixFile'): # TODO
		for counter in  self.counters.items():
			print "\n",counter[0]
			print "-" * len(counter[0])
			print counter[1]
			#print "\tNumber of parts: %d\n\tTotal submits: %d" % (counter['parts'], counter['submits'] )
			

	def listCountersFiles(self):
		return self.__counters_files 

	def verifyCounterFile(self, fd):
		Boolean = self.__is_a_CounterFile(fd)
		if Boolean :
			print "%s : is a valid counter file with content %s" % (fd, self.__chk_counter_content(fd))
		else:
			print "%s : is not a valid counter file" % (fd,)
		return Boolean

	def __chk_counter_metaData(self, file_name):
		file_name = path.basename(file_name)
		pid, day, month, year, smsc = file_name.split('.')
		try:
			return filter(int, [pid, day, month, year]), smsc
		except ValueError :
			raise CollectorException("Could not get counter : \"%s\" metadata" % (file_name,),1)
	
	def __chk_counter_content(self, _file):
		if isinstance(_file, file):  # fd 
			file_name = _file.name
		else: # fs path
			file_name = _file
		with open(file_name) as f :
			try :
				counter = marshal.load(f)
			except :
				##@DEBUG
				print "this is not proper file", file_name
		for key in counter:
			if key in ('parts', 'submits') and isinstance(counter[key], int):
				continue
			else:
				print ">>>>%s,%s->%s".format(key, counter, file_name)
				raise self.CollectorException("ContentError -> Invalid counter structure  %s " % (file_name,),2)
		return counter

	def __is_a_CounterFile(self, file_name):
		if file_name == None :
			return False 
		try: 
			self.__chk_counter_metaData(file_name) #duplicated when called from iterator
			self.__chk_counter_content(file_name)
			return True
		except self.CollectorException("COUNTER ERROR",2) as e:
			print "Counter Error : {0}" .format(e.strerror)
			return False
		except:
			print "Other exception at __is_a_CounterFile() %s" % (file_name,)
			return False 

	def __load_counter(self, FILENAME):
		""" get counter from count file i.e. 24172.29.09.2014.mobily"""
		if not self.__is_a_CounterFile(FILENAME): #Not a counter
			return #self.counters
		smsc = self.__chk_counter_metaData(FILENAME)[-1]
		counter = self.__chk_counter_content(FILENAME)
		if self.counters.has_key(smsc): # accumulate to existing counter
			self.counters[smsc]['parts'] += counter['parts']
			self.counters[smsc]['submits'] += counter['submits']
		else: # load new counter
			self.counters[smsc] =  counter
		return self.counters



def main(argv):
	"""
		Usage :
		Valide optoins : 
			"-L == list-countersFiles ,-v == version, -c == check-counterfile, -f == from-date ,-t == to-date ,-m == month ,-l == link ,-h --help ,-d == dump-config"
			getopt args ("c:f:t:m:l:hvLd", ["check-counterfile" ,"from-date" ,"to-date" ,"month" ,"link" ,"help" ,"version" ,"list-countersFiles", "dump-config"])
		examples :
		     # python collect_counters.py # collect today counters
		     # python collect_counters.py -f 20012014 -t 22012014
		or   # python collect_counters.py -m 4 -l link12

	"""
	smsc = month = end = start = None 
	list_flag = False
	try:
		#opts, args = getopt.getopt(argv,"c:f:t:m:l:hvLd", ["check-counterfile" ,"from-date" ,"to-date" ,"month" ,"link" ,"help" ,"version" ,"list-countersFiles", "dump"])
		opts, args = getopt.getopt(argv, "c:f:t:m:l:hvLd" )
	except getopt.GetoptError:
		print main.__doc__
		sys.exit(1)
	for opt, arg in opts:
		if opt in ("-d", "--dump"):
			c = Collector()
			c.dump()
			return 0
		elif opt in ("-L", "--list-countersFiles"):
			print "Counter Files :"
			list_flag = True
			continue
		elif opt in ("-c", "--check-counterfile"):
			c = Collector()
			c.verifyCounterFile(arg)
			return 0
		elif opt in ("-v", "--version"):
			print "Version 1 Check git"
			return 0
		elif opt in ("-h", "--help"):
			print main.__doc__ 
			exit(0)
		elif opt in ("-l", "--link"):
			smsc = arg
			continue
		elif opt in ("-m" ,"--month"):
			month = arg
			continue
		elif opt in ("-t", "--to-date"):
			end = arg
			continue
		elif opt in ("-f", "--from-date"):
			start = arg
			continue
		else:
			print main.__doc__ 
			exit(1)
	#print "smsc:%s, month:%s ,start:%s ,end:%s" %(smsc,month,start,end)
	c = Collector(smsc, month, start, end)
	if list_flag :
		for f in c.listCountersFiles() :
			print f
	import json
	print c.count()
	print "JSON format"
	print "-----------"
	print json.dumps(c.count(), sort_keys=True, indent=4, separators=(',', ': '))


	
if __name__ == "__main__" :
	main(sys.argv[1:])
	# test(sys.argv[1:])
