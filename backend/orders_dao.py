from datetime import datetime
from sql_connection import get_sql_connection

def insert_new_order(connection, order):
    cursor = connection.cursor()

    # Insert into orders table
    order_query = (
        "INSERT INTO orders (customer_name, total, datetime) "
        "VALUES (%s, %s, %s)"
    )
    order_data = (
        order['customer_name'],
        order['grand_total'],
        datetime.now()
    )
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    # Insert into order_details table
    order_details_query = (
        "INSERT INTO order_details (order_id, product_id, quantity, total_price) "
        "VALUES (%s, %s, %s, %s)"
    )
    order_details_data = []

    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])

    cursor.executemany(order_details_query, order_details_data)
    connection.commit()
    return order_id


# def get_all_orders(connection):
#     cursor = connection.cursor()
#     query = "SELECT * FROM orders"
#     cursor.execute(query)

#     response = []
#     for (order_id, customer_name, total, datetime_value) in cursor:
#         response.append({
#             'order_id': order_id,
#             'customer_name': customer_name,
#             'total': total,
#             'datetime': datetime_value.strftime("%Y-%m-%d %H:%M:%S")
#         })
# def get_all_orders_with_items(connection):
#     cursor = connection.cursor(dictionary=True)

#     # Get all orders
#     cursor.execute("SELECT * FROM orders")
#     orders = cursor.fetchall()

#     # Get all order items
#     cursor.execute("""
#         SELECT oi.order_id, p.name, oi.quantity, oi.price_pre_unit
#         FROM order_items oi
#         JOIN products p ON oi.product_id = p.product_id
#     """)
#     items = cursor.fetchall()

#     # Group items by order_id
#     from collections import defaultdict
#     order_items_map = defaultdict(list)
#     for item in items:
#         order_items_map[item['order_id']].append({
#             'product_name': item['name'],
#             'quantity': item['quantity'],
#             'price_pre_unit': item['price_pre_unit']
#         })

#     # Add items to corresponding orders
#     for order in orders:
#         order['items'] = order_items_map.get(order['order_id'], [])

#     return orders


#     return response
# def get_all_orders_with_items(connection):
#     cursor = connection.cursor(dictionary=True)

#     # Get all orders
#     cursor.execute("SELECT * FROM orders")
#     orders = cursor.fetchall()

#     # Get all order items with product names
#     cursor.execute("""
#         SELECT oi.order_id, p.name, oi.quantity, oi.price_pre_unit
#         FROM order_details oi
#         JOIN products p ON oi.product_id = p.product_id
#     """)
#     items = cursor.fetchall()

#     # Group items by order_id
#     from collections import defaultdict
#     order_items_map = defaultdict(list)
#     for item in items:
#         order_items_map[item['order_id']].append({
#             'name': item['name'],
#             'quantity': item['quantity'],
#             'price': item['price_pre_unit']
#         })

#     # Attach items to corresponding orders
#     for order in orders:
#         order['items'] = order_items_map.get(order['order_id'], [])

#     return orders
# def get_all_orders_with_items(connection):
#     cursor = connection.cursor(dictionary=True)

#     # ✅ Step 1: Fetch all orders
#     cursor.execute("SELECT * FROM orders")
#     orders = cursor.fetchall()

#     # ✅ Step 2: Fetch all items from order_details
#     cursor.execute("""
#         SELECT od.order_id, p.name, od.quantity, od.price_pre_unit
#         FROM order_details od
#         JOIN products p ON od.product_id = p.product_id
#     """)
#     items = cursor.fetchall()

#     # ✅ Step 3: Group items by order_id
#     from collections import defaultdict
#     order_items_map = defaultdict(list)
#     for item in items:
#         order_items_map[item['order_id']].append({
#             'product_name': item['name'],
#             'quantity': item['quantity'],
#             'price_pre_unit': item['price_pre_unit']
#         })

#     # ✅ Step 4: Add items to each order
#     for order in orders:
#         order['items'] = order_items_map.get(order['order_id'], [])
#         order['datetime'] = order['datetime'].strftime("%Y-%m-%d %H:%M:%S")

#     return orders
# def get_all_orders_with_items(connection):
#     cursor = connection.cursor(dictionary=True)

#     # Step 1: Fetch all orders
#     cursor.execute("SELECT * FROM orders")
#     orders = cursor.fetchall()

#     # Step 2: Fetch order items from order_details + join with products to get name & price
#     cursor.execute("""
#         SELECT od.order_id, p.name, od.quantity, p.price_pre_unit
#         FROM order_details od
#         JOIN products p ON od.product_id = p.product_id
#     """)
#     items = cursor.fetchall()

#     # Step 3: Group items by order_id
#     from collections import defaultdict
#     order_items_map = defaultdict(list)
#     for item in items:
#         order_items_map[item['order_id']].append({
#             'product_name': item['name'],
#             'quantity': item['quantity'],
#             'price_pre_unit': item['price_pre_unit']
#         })

#     # Step 4: Add items to each order
#     for order in orders:
#         order['items'] = order_items_map.get(order['order_id'], [])
#         order['datetime'] = order['datetime'].strftime("%Y-%m-%d %H:%M:%S")

#     return orders
def get_all_orders_with_items(connection):
    cursor = connection.cursor(dictionary=True)

    # Step 1: Get all orders
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    # Step 2: Get order items with price from products
    cursor.execute("""
        SELECT od.order_id, p.name, od.quantity, p.price_pre_unit
        FROM order_details od
        JOIN products p ON od.product_id = p.product_id
    """)
    items = cursor.fetchall()

    # Step 3: Group items by order_id and calculate subtotals
    from collections import defaultdict
    order_items_map = defaultdict(list)
    grand_totals = defaultdict(float)

    for item in items:
        # subtotal = item['quantity'] * item['price_pre_unit']
        subtotal = float(item['quantity']) * float(item['price_pre_unit'])

        order_items_map[item['order_id']].append({
            'product_name': item['name'],
            'quantity': item['quantity'],
            'price_pre_unit': item['price_pre_unit'],
            'subtotal': subtotal
        })
        grand_totals[item['order_id']] += subtotal

    # Step 4: Add items + grand_total to each order
    for order in orders:
        order_id = order['order_id']
        order['items'] = order_items_map.get(order_id, [])
        order['grand_total'] = grand_totals.get(order_id, 0.0)
        order['datetime'] = order['datetime'].strftime("%Y-%m-%d %H:%M:%S")

    return orders



# 🔍 Optional testing block
if __name__ == '__main__':
    connection = get_sql_connection()

    new_order_id = insert_new_order(connection, {
        'customer_name': 'lokesh',
        'grand_total': 500,
        'order_details': [
            {
                'product_id': 1,
                'quantity': 2,
                'total_price': 50
            },
            {
                'product_id': 3,
                'quantity': 1,
                'total_price': 30
            }
        ]
    })
    print(f"✅ Inserted order ID: {new_order_id}")

    all_orders = get_all_orders(connection)
    print(f"📦 All Orders: {all_orders}")
