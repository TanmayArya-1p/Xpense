import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
        
        
        
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

import requests

def CheckUnUsr(uid):
    key = GetConfig()["SERVER"]["KEY"]
    ip = f"{GetConfig()['SERVER']['HOST']}/getuids/?key={key}"
    r = requests.post(ip)
    for i in r.json():
        if(str(uid) == str(i[0])):
            return False
    return True
    
def RegisterUser(uname,uid,pwd):
	key = GetConfig()["SERVER"]["KEY"]
	headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
	}
	params = {
		'key': '123',
	}
	json_data = {
		'uname': uname,
		'uid': uid,
		'pwd_hash': pwd,
		'login': 'stri2214124ng',
	}

	response = requests.post(f"{GetConfig()['SERVER']['HOST']}/register/", params=params, headers=headers, json=json_data)