import configparser



class AutoRepr:
	def __repr__(self):
		otpt = ""
		for i in self.__dict__:
			otpt = otpt+str(i)+"="
			if(type(self.__dict__.get(i)) == str):
				otpt=otpt+ '"'+ str(self.__dict__.get(i))+'"' + " , "
			else:
				otpt=otpt+ str(self.__dict__.get(i)) + " , "
		otpt = otpt[:-3]
		rtn = f'{self.__class__.__name__}({otpt})'
		return rtn

def GetConfig():
	cp = configparser.ConfigParser()
	cp.read("config.ini")
	return dict(cp)

