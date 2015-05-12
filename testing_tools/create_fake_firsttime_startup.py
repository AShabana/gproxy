import os
import pickle
print "This script MUST run from script directory "


accounts = ( 'ahmed' ,'ali' ,'omar')
with open('../config/lists/accounts','wb') as fd :
       pickle.dump(accounts, fd)
       
config_data = """ 
logic = "KannelProxy"
lists = "config/lists/accounts"
counter-path = "counters"
ports = "2014,2015,2016,2017,2018"
log-file = "/var/log/GProxy.log"
pid-file = "listener.pid"
"""

with open('../config/app.conf', 'w') as config_file :
    config_file.write(config_data)
		 
