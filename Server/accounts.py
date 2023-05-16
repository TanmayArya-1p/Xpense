import mysql.connector
from util import *
from pydantic import BaseModel
from defs import *
from errors import *
import datetime
import json
import dataclasses
STANDARD_SCHEMA = {"expenditure":0,"orders":["placeholder"],"recently_bought":["placeholder"]}


class UserTable(AutoRepr):
  def __init__(self,host,user,pwd):
    self.user = user
    self.pwd = pwd
    self.host = host
    self.database = mysql.connector.connect(
    host =host,
    user =user,
    passwd =pwd
    )
    self.co = self.database.cursor()
    self.initiate_table()
      
  def initiate_table(self):
    with open("initiate.txt" , "r") as r:
      for i in r.readlines():
        self.co.execute(i)
    self.database.commit()
  

  def register_user(self,key,usr):
    if(key == GetConfig()["SERVER"]["KEY"]):
      print(usr)
      print(datetime.datetime.now())
      result = self.co.execute(f"insert into users values('{usr.uid}','{usr.uname}','{usr.pwd_hash}','123')")
      usr.initiate_item_file()
      self.database.commit()
      return result
    else:
      print("awfnhjwabgwaygbawg")
      return "Invalid Key"
    
  def delete_user(self,key,usr):
    print(GetConfig()["SERVER"]["KEY"])
    if(key == GetConfig()["SERVER"]["KEY"]):
      result = self.co.execute(f"delete from users where id = '{usr.uid}'")
      self.database.commit()
      return result
    else:
      return "Invalid Key"
  
  def fetch_all(self,key):
    if(key == GetConfig()["SERVER"]["KEY"]):
      self.co.execute("select * from users")
      return self.co.fetchall()
    else:
      return "Invalid Key"

  def fetch_udata(self,key,uid):
    if(key == GetConfig()["SERVER"]["KEY"]):
      self.co.execute(f"select * from users where id='{uid}'")
      try:
        with open(f"Userdata/{uid}.json", "r") as f:
          return {"udata" : User.get_udata(uid) , "meta"  : self.co.fetchall()}
      except:
        return"Not Found"
    else:
      return "Invalid Key"
    
  def get_uids(self,key):
    if(key == GetConfig()["SERVER"]["KEY"]):
      self.co.execute("select id from users")
      return self.co.fetchall()
    else:
      return "Invalid Key"
    
  def alter_udata(self,key,uid,udata):
    if(key == GetConfig()["SERVER"]["KEY"]):
      print(udata)
      with open(f"Userdata/{uid}.json", "w") as f:
        f.write(json.dumps(udata))
        f.close()
      return udata
    else:
      return "Invalid Key"


