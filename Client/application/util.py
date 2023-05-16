import configparser
def GetConfig():
	cp = configparser.ConfigParser()
	cp.read("config.ini")
	return dict(cp)


