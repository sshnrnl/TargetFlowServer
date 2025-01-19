from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/v1/sales/items-list', methods=['get'])
@token_required
def get_items_list():
    conn = connect()
    cursor = conn.cursor()
    query="SELECT KOBAR,NAMBAR,HJUAL,KOSAT from KOBAR"
    cursor.execute(query)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({
        "status":200,
        "message":"You have collected items list",
        "result":result
    })