from flask import Flask, Response
from routes import tables, menus, orders
from db import get_db
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def test_connect_api():
    response = Response()
    return response

app.register_blueprint(tables.table_app, url_prefix="/table")
app.register_blueprint(menus.menu_app, url_prefix="/menu")
app.register_blueprint(orders.order_app, url_prefix="/order")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)