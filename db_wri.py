#coding: utf-8
from peewee import *
import configparser as cparser


cp = cparser.ConfigParser()
cp.read("db.ini")
db = MySQLDatabase(
    host=cp.get("mysqlconf", "host"),
    port=cp.getint("mysqlconf", "port"),
    user=cp.get("mysqlconf", "user"),
    #passwd=cp.get("mysqlconf", "password"),
    database=cp.get("mysqlconf", "db_name"),
    
)
db.connect()

class BaseModel(Model):
    class Meta:
        database = db
        
class Lagou(BaseModel):
    city = CharField()
    company = CharField()
    position = CharField()
    salary = CharField()
    

    
    



    