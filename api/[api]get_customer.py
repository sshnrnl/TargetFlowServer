from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/v1/sales/customer-list', methods=['get'])
@token_required
def get_customer_list():
    conn = connect()
    cursor = conn.cursor()
    query="SELECT FIRST 100 KOCUS,NAMCUS from KOCUS"
    cursor.execute(query)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({
        "status":200,
        "message":"You have collected customer list",
        "result":result
    })

@app.route('/api/v1/sales/customer-details', methods=['POST'])
@token_required
def get_customer_details():
    request_data = request.json
    kocus=request_data['customer_id']

    conn = connect()
    cursor = conn.cursor()
    query = """
            SELECT 
                KOCUS, 
                NAMCUS, 
                COALESCE(ALIAS, NAMCUS) AS ALIAS_OR_NAME, 
                COALESCE(ALAMAT1, '-') AS ALAMAT,
                COALESCE(TELP, '-') AS TELP 
            FROM KOCUS 
            WHERE KOCUS = ?;
        """
    cursor.execute(query, (kocus,))
    result=cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return jsonify({
        "status":200,
        "message":"You have collected customer details",
        "result":result
    })