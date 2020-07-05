from flask import Flask, render_template, request, redirect, Response
from werkzeug.exceptions import HTTPException
import json
from db import table_coll
from datetime import datetime

from flask import Blueprint

table_app = Blueprint('table', __name__)

@table_app.route('/add-table', methods=['POST'])
def add_table():
    data = request.get_json()
    check = table_coll.find({"$or": [{"org_table_id": data["org_table_id"]}, {"org_table_name": data["org_table_name"]}]}, {"_id": False, "created_at": False, "updated_at": False})
    if list(check):
        return Response(status=409)
    data.update({"created_at": datetime.now(), "updated_at": datetime.now()})
    table_coll.insert_one(data)
    return Response(status=200)

@table_app.route('/edit-table/<table_id>', methods=['PUT'])
def edit_table(table_id):
    if table_id:
        return Response(status=404)
    else:
        data = request.get_json()
        data.update({"updated_at": datetime.now()})
        table_coll.update({"org_table_id": table_id}, {"$set" : data}, False)
        return Response(status=204)

@table_app.route('/delete-table/<table_id>', methods=['DELETE'])
def delete_table(table_id):
    if table_id == None:
        return Response(status=404)
    else:
        table_coll.remove({"org_table_id": table_id})
        return Response(status=202)

@table_app.route('/get/table/qty', methods=["GET"])
def table_qty():
    a = list(table_coll.aggregate([
        {
        "$group":
            {
                "_id": {  },
                "totalAmount": { "$sum": "$current_qty" },
            }
        }
    ]))
    if a:
        qty = a[0]["totalAmount"]
        return str(a), 200
    else:
        return str("No Tables Found"), 200

@table_app.route('/get/all', methods=["GET"])
def get_all_table():
    data = list(table_coll.find({}, {"_id": False, "created_at": False, "updated_at": False}))
    return json.dumps(data), 200