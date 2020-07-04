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

@order_app.route('/change/order-status/<order_id>/status/<status>', methods=["PUT"])
def change_order_status(order_id, status):
    order_coll.update({"order_id": order_id}, {"set": {"status": status}}, False)
    return Response(status=204)

@order_app.route('/get/order/<status>', methods=["GET"])
def ongoing_order(status):
    data = list(order_coll.find({"status": status}))
    return json.dumps(data), 200