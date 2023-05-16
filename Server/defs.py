from util import *
from pydantic import BaseModel
import datetime
import json
import dataclasses
from typing import List, Optional
import mysql.connector



STANDARD_SCHEMA = {"expenditure":0,"orders":["placeholder"],"recently_bought":["placeholder"]}

@dataclasses.dataclass()
class UserTable:
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

class User(BaseModel):
  uname: str
  uid: str
  pwd_hash: str
  login: str
  utable: Optional[UserTable]
  
  def logged(self):
    self.utable.co.execute(f"update users set lastlogin='{datetime.datetime.now()}'")

  def change_uname(self,new):
    self.utable.co.execute(f"update users set uname='new'")
  
  def initiate_item_file(self):
    with open(f"Userdata/{self.uid}.json", "w") as f:
      f.write(json.dumps(STANDARD_SCHEMA))
      f.close()
  
  @staticmethod
  def get_udata(uid):
    with open(f"Userdata/{uid}.json" , "r") as f:
      return json.load(f)
  
