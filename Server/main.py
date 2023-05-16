from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from defs import *
from accounts import *
from errors import *
from typing import Dict,Any

u = UserTable("localhost","root","pvcs")
app = FastAPI()

@app.get("/")
async def root():
    return True

@app.post("/register/")
async def register_user(key,user: User):    
    u.register_user(key,user)
    return user

@app.post("/deleteuser/")
async def delete_user(key,user: User):
    u.delete_user(key,user)
    return user

@app.post("/fetchusers/")
async def fetch_all(key):
    return u.fetch_all(key)

@app.post("/fetchudata/")
async def fetch_udata(key,uid):
    return u.fetch_udata(key,uid)


@app.post("/getuids/")
async def getuids(key):
    return u.get_uids(key)


@app.post("/alterudata/")
async def alterudata(key,uid,udata : Dict[str,Any]):
    return u.alter_udata(key,uid,udata)

import requests
@app.get("/convert")
async def convert(key,currin,currout):
    r= requests.get(f"https://api.currencyapi.com/v3/latest?apikey=z6LsLtB7v436ET91gHyVryDZc8wKXlA0iE2J8rzM&currencies={currin.upper()}&base_currency={currout.upper()}")
    print(r.status_code)
    print(r.json())
    return r.json()