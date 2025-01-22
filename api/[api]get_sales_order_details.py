from api.index import app, connect, jwt, request, jsonify, token_required
import os

SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/v1/sales/sales-order-details', methods=['GET'])
@token_required
def get_sales_order_details():
    # Retrieve query parameter
    filter_param = request.args.get('so_id', default=None)

    # Validate filter_param
    if not filter_param:
        return jsonify({
            "status": 400,
            "message": "Parameter 'param' is required"
        }), 400

    # Establish database connection
    conn = connect()
    cursor = conn.cursor()

    # Use parameterized query to avoid SQL injection
    query = "SELECT NOBUK, TGL, KOCUS, NAMCUS, JUMLAH, NET, JTEMPO FROM MSO WHERE NOBUK = ?"
    cursor.execute(query, (filter_param,))

   
    # Fetch results
    nobuk,tgl,kocus,namcus,jumlah,net,jtempo = cursor.fetchall()[0]

    #get all items in mso
    items=get_sales_order_items(cursor, filter_param)

    # Close cursor and connection
    cursor.close()
    conn.close()

    return jsonify({
        "status": 200,
        "message": "You have collected the items list",
        "result": {
            "sales_order":{
                "nobuk":nobuk,
                "tgl":tgl,
                "kocus":kocus,
                "namcus":namcus,
                "jumlah":jumlah,
                "net":net,
                "jtempo":jtempo
            },
            "items":items
        }
    })

    


def get_sales_order_items(cursor, nobuk):
    query = "SELECT KOBAR, COALESCE(NAMBAR, 'Undefined'), QTY, SATQTY, JUMLAH FROM MUTSO WHERE NOBUK = ?"
    cursor.execute(query, (nobuk,))
    return cursor.fetchall()