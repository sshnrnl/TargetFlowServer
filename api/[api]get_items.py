from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os

SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/v1/sales/items-list', methods=['GET'])
@token_required
def get_items_list():
    conn = connect()
    cursor = conn.cursor()
    query = """
        SELECT 
            K.KOBAR,
            K.NAMBAR,
            K.HJUAL,
            K.KOSAT,
            T.KVRSI,
            COALESCE(K.MINHJUAL, K.HJUAL) AS MINHJUAL
        FROM 
            KOBAR K
        LEFT JOIN 
            TBKVRSI T ON K.KOBAR = T.KOBAR
        WHERE 
            COALESCE(K.NONAKTIF, '') != 'T'
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({
        "status": 200,
        "message": "You have collected items list",
        "result": result
    })
