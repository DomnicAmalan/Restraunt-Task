from flask import Flask, render_template, request, redirect, Response
from werkzeug.exceptions import HTTPException
import json
from db import order_coll

from flask import Blueprint

order_app = Blueprint('order', __name__)

@order_app.route('/add-order', methods=['POST'])
def add_order():
    data = request.get_json()
    order_coll.insert(data)
    return Response(status=200)

@order_app.route('/change/order-status/<order_id>', methods=["PUT"])
def change_order_status(order_id):
    data = request.get_json()
    print(data)
    order_coll.update({"order_id": data}, {"set": {"status": data["order_status"]}}, False)
    return Response(status=204)

@order_app.route('/get/order/<status>', methods=["GET"])
def ongoing_order(status):
    data = list(order_coll.find({"status": status}, {"_id": False, "created_at": False, "updated_at": False}))
    return json.dumps(data), 200

@order_app.route('/get/order/count', methods=["GET"])
def get_count_order():
    data = order_coll.count()
    return str(data), 200

@order_app.route('/get/order/all', methods=["GET"])
def all_orders( ):
    data = list(order_coll.find({}, {"_id": False, "created_at": False, "updated_at": False}))
    return json.dumps(data), 200