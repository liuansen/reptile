# _*_ coding: utf-8 _*_

from pymongo import MongoClient

client = MongoClient()
db = client.test
my_set = db.set

my_set.insert({"name": "yyy", "age": 18})
