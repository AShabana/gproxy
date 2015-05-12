import os
import pickle
print "This script MUST run from script directory "
# Create fake runtime list if not exist
if not os.path.exists('../config/lists'):
	os.makedirs('../config/lists')
if not os.path.exists('../config/lists/accounts') :
	accounts = ( 'ahmed' ,'ali' ,'omar')
	with open('../config/lists/accounts','wb') as fd :
		pickle.dump(accounts, fd)
# Create config file if not exist
config_data = """ 
logic = "KannelProxy"
lists = "config/lists/accounts"
counter-path = "counters"
ports = "2014,2015,2016,2017,2018"
log-file = "/var/log/GProxy.log"
pid-file = "listener.pid"
"""
if not os.path.exists('../config/app.conf') :
	with open('../config/app.conf', 'w') as config_file :
    		config_file.write(config_data)
# Create SHM Segment for runtime counter
if not os.path.exists("/dev/shm/gproxy"):
	os.makedirs("/dev/shm/gproxy")
if not os.path.exists("/dev/shm/gproxy/counters"):
	os.makedirs("/dev/shm/gproxy/counters")
# Create prisist storage for runtime counter
if not os.path.exists("../counters"):
	os.makedirs("../counters")
