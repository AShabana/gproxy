import pickle 

class GPLists:
    def __init__(self, path=None):
        self.__listsFile = "config/lists/all.py" if path == None else path
        #self.__listsFile = "config/lists/all.py" # if path == None else path
        self.__gplists = {} # to confirm for any farther implementations this is hash array
        self.__gplists = self.__loadlists()
    
    def __loadlists(self): # implement any i.e. marshal, sqlite  ,.... etc
        with open(self.__listsFile, "r") as fd :
            return pickle.load(fd)

    def __savelists(self): # implement any i.e. marshal, sqlite  ,.... etc
        with open(self.__listsFile, "wb") as fd :
            pickle.dump(self.__gplists ,fd)

    def load(self):
    	return self.__gplists

    def listall(self):
        listidx = self.__gplists.keys()
        return listidx

    def listlist(self, listid):
        gplist = self.__gplists[listid]
        return gplist

    def addtolist(self, sender, listid):
    	if sender in self.__gplists[listid]:
		return "Error: Sender already registered!"
        self.__gplists[listid].append(sender)
        self.__savelists()
        return "Done."

    def addlist(self, listname):
    	if self.__gplists.has_key(listname) :
		return 'List already exist'
	self.__gplists[listname] = []
	self.__savelists()
	return "Done."

    def dellist(self, listname):
    	if not self.__gplists.has_key(listname) :
		return 'List not exist'
    	self.__gplists.pop(listname)
	self.__savelists()
	return 'Done.'

    def delfromlist(self, sender_del, listid_del):
    	if sender_del in self.__gplists[listid_del]:
            self.__gplists[listid_del].remove(sender_del) if sender_del in self.__gplists[listid_del] else None
            self.__savelists()
            return "done"
	else :
	    return "Error Sender not found in list tobe deleted!"


def main(argv):
	"""
		Usage :
		Valide optoins : 
			--show-lists , --show-list listName ,--addto-list listName itemName ,  --add-list listName, --rm-frmList listName itemName, --rm-list listName = --del-list listName
		     
	"""
	try:
		opts, args = getopt.getopt(argv,"", ["show-lists" ,"show-list" ,"addto-list" ,"addbulk" ,"add-list" ,"rm-frmList","del-list","rm-list"])
	except getopt.GetoptError:
		print main.__doc__
		sys.exit(1)
	for opt, arg in opts:
		if opt == "--show-lists" :
				gplists = GPLists()
				print gplists.listall()
				exit(0)
		elif opt == "--show-list" :
				gplists = GPLists()
				listid = args[0]
				print gplists.listlist(listid)
				exit(0)
		elif opt == "--addto-list":
				gplists = GPLists()
				listid = args[0]
				item = args[1]
				print gplists.addtolist(item, listid)
				exit(0)
		elif opt == "--rm-frmList":
				gplists = GPLists()
				listid = args[0]
				item = args[1]
				print gplists.delfromlist(item, listid)
				exit(0)
		elif opt == "--add-list" :
				gplists= GPLists()
				listid = args[0]
				print "Add new list %s" , (listid,)
				gplists.addlist(listid)
				exit(0)
		elif opt == "--del-list" :
				gplists = GPLists()
				listid = args[0]
				print "Remove list %s"  , (listid,)
				gplists.dellist(listid)
				exit(0)
		elif opt == "--rm-list":
				gplists = GPLists()
				listid = args[0]
				print "Remove list %s"  , (listid,)
				gplists.dellist(listid)
				exit(0)
		else :
				print "Invalid option"
				print main.__doc__
				exit(0)


if __name__ == "__main__" :
		from sys import argv
		import sys
		import getopt

		main(argv[1:])
