from flask import Flask, render_template, request, redirect, Response
from werkzeug.exceptions import HTTPException
import json
from db import menu_coll, menu_item_coll
from datetime import datetime

from flask import Blueprint

menu_app = Blueprint('menu', __name__)

@menu_app.route('/add-menu-category', methods=['POST'])
def add_category():
    data = request.get_json()
    check = menu_coll.find_one({"$or": [{"name": data["name"]}, {"org_id_category": data["org_id_category"]}]}, {"_id": False, "created_at": False, "updated_at": False})
    if list(check):
        return Response(status=409)
    data.update({"created_at": datetime.now(), "updated_at": datetime.now()})
    menu_coll.insert(data)
    return Response(status=200)

@menu_app.route('/update-menu-category/<category_id>', methods=['PUT'])
def update_category(category_id):
    if category_id == None:
        return Response(status=404)
    else:
        data = request.get_json()
        data.update({"updated_at": datetime.now()})
        menu_coll.update({"org_id_category": category_id}, {"$set": data}, False)
        return Response(status=204)

@menu_app.route('/delete-menu-category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id == None:
        return Response(status=404)
    else:
        menu_coll.remove({"org_table_id": category_id})
        return Response(status=202)

@menu_app.route('/add-items', methods=['POST'])
def add_items():
    data = request.get_json()
    check = menu_item_coll.find({"$or": [{"org_item_id": data["org_item_id"]}, {"name": data["name"]}]}, {"_id": False, "created_at": False, "updated_at": False})
    if list(check):
        return Response(status=409)
    data.update({"created_at": datetime.now(), "updated_at": datetime.now()})
    menu_item_coll.insert_one(data)
    return Response(status=200)

@menu_app.route('/update-items/<item_id>', methods=['PUT'])
def update_items(item_id):
    if item_id == None:
        return Response(status=409)
    else:
        data = request.get_json()
        data.update({"updated_at": datetime.now()})
        id = menu_item_coll.update({"org_item_id": str(item_id)}, {"$set": data})
        return Response(status=204)

@menu_app.route('/delete-items/<item_id>', methods=["DELETE"])
def delete_item(item_id):
    if item_id == None:
        return Response(status=404)
    else:
        menu_item_coll.remove({"org_item_id": str(item_id)})
        return Response(status=202)

@menu_app.route('/get/all', methods=["GET"])
def get_menu_items():
    data = list(menu_item_coll.find({}, {"_id": False, "created_at": False, "updated_at": False}))
    print(data)
    if data:
        return json.dumps(data), 200
    else:
        return Response(status=204)