from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = ("SELECT products.product_id, products.name, products.uom_id, products.price_pre_unit, uom.uom_name "
         "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id "
         "WHERE products.is_active = TRUE")

    #query = (
     #   "SELECT products.product_id, products.name, products.uom_id, "
      #  "products.price_pre_unit, uom.uom_name "
       # "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id"
    #)

    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_pre_unit, uom_name) in cursor:
        response.append(
            {
                'product_id':product_id,
                'name':name,
                'uom_id':uom_id,
                'price_pre_unit':price_pre_unit,
                'uom_name':uom_name

            }
        )


    return response
def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = (
        "INSERT INTO products (name, uom_id, price_pre_unit) "
        "VALUES (%s, %s, %s)")
    data=(product['product_name'],product['uom_id'],product['price_pre_unit'])
    cursor.execute(query,data)
    connection.commit()
    return cursor.lastrowid
#def delete_product(connection,product_id ):
 #   cursor=connection.cursor()
  #  query=("DELETE FROM products where product_id"+str(product_id))
   # cursor.execute(query)
    #connection.commit
    
#def delete_product(connection, product_id):
  #  cursor = connection.cursor()
   # query = "DELETE FROM products WHERE product_id = %s"
  #  cursor.execute(query, (product_id,))
   # connection.commit()
    #return product_id
#def delete_product(connection, product_id):
#    cursor = connection.cursor()
 #   query = "UPDATE products SET is_active = FALSE WHERE product_id = %s"
 #   cursor.execute(query, (product_id,))
 #   connection.commit()
 #   return product_id
def delete_product(connection, product_id):
    try:
        cursor = connection.cursor()
        query = "UPDATE products SET is_active = FALSE WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        connection.commit()
        return True
    except Exception as e:
        print("❌ Error in delete_product:", e)
        return False


if __name__ == '__main__':
    connection=get_sql_connection()
    print(insert_new_product(connection,{
        'product_name': 'orange',
        'uom_id': 1,
        'price_pre_unit': 10
    }))