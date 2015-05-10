##block of Config conversion (migrateLists_v2.2.py)
#1 Migrate lists
import pickle 
import configobj 
import imp
Config = imp.load_source('Config', "/root/CCSKannelProxy_V2.1/gproxy/config/lists/all.py")
import Config
lists = (l for l in dir(Config) if not l.startswith('__') )
cnf = {}
for li in lists :
	#print eval('Config.' + li )
	x =  eval('Config.' + li )
	cnf[li] = list(x) 
with open("config/lists/all.py", 'wb') as f :
	pickle.dump(cnf,f)
print "Done. "
exit(0)

#for i in /root/CCSKannelProxy_V2.1/gproxy/runtime/*.py
#do
#	cat $i  | perl -pe 's/Config\.([0-9A-Za-z_]+)/Config\[$1\]/g' > runtime/$i
#done 
