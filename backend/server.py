# from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template

from flask_cors import CORS
import json
import products_dao
import uom_dao
import orders_dao
from sql_connection import get_sql_connection
from products_dao import insert_new_product


app = Flask(__name__, template_folder='templates',   # explicitly set templates folder
    static_folder='static')
CORS(app)

connection = get_sql_connection()
# @app.route('/')
# def index():
#     return render_template('index.html')  # or change if your main file is named differently
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/view-orders')
def view_orders():
    return render_template('view_orders.html')

@app.route('/manage-product')
def manage_product():
    return render_template('manage-product.html')




# 🟢 Get all products
@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    return jsonify(products)

# 🟢 Get all units of measurement
@app.route('/getUOM', methods=['GET'])
def get_uom():
    uoms = uom_dao.get_uoms(connection)
    return jsonify(uoms)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    try:
        data = request.get_json()
        name = data['product_name']   # use 'product_name' to match your JS payload
        price_pre_unit = data['price_pre_unit']
        uom_id = data['uom_id']

        result = insert_new_product(connection, {
            'product_name': name,
            'price_pre_unit': price_pre_unit,
            'uom_id': uom_id
        })
        return jsonify({'status': 'success', 'product_id': result})
    except Exception as e:
        print("❌ Error in insert_product:", e)
        return jsonify({'error': str(e)}), 400


# 🟢 Delete product using JSON
@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    try:
        request_payload = request.get_json()
        print("🔍 Delete Product Payload:", request_payload)
        product_id = request_payload['product_id']
        return_id = products_dao.delete_product(connection, product_id)
        return jsonify({'product_id': return_id})
    except Exception as e:
        print("❌ Error in delete_product:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 400

# 🟢 Insert an order
@app.route('/insertOrder', methods=['POST'])
def insert_order():
    try:
        request_payload = request.get_json()
        print("📝 Order payload:", request_payload)
        order_id = orders_dao.insert_new_order(connection, request_payload)
        return jsonify({'order_id': order_id})
    except Exception as e:
        print("❌ Error in insert_order:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 🟢 Get all orders with their items
@app.route('/getOrderDetails', methods=['GET'])
def get_order_details():
    try:
        orders = orders_dao.get_all_orders_with_items(connection)
        return jsonify(orders)
    except Exception as e:
        print("❌ Error in get_order_details:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting Flask server for Grocery Store Management System...")
    app.run(port=5051, debug=True)
