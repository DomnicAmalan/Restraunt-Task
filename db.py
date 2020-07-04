import pymongo
from functools import wraps
from flask import request, Response
from pymongo.errors import ConnectionFailure

def get_db():
    try:
        client = pymongo.MongoClient("localhost", 27017, serverSelectionTimeoutMS=500)
        db = client["toast"]
        return db
    except ConnectionFailure:
        return "Server not available"

table_coll = get_db()["tables"]
order_coll = get_db()["orders"]
menu_coll = get_db()["menus"]
menu_item_coll = get_db()["menu_items"]