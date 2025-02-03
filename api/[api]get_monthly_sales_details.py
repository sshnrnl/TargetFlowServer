from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os
from datetime import datetime, timedelta, timezone
SECRET_KEY = os.getenv("SECRET_KEY")
@app.route('/api/v1/sales/get_monthly_sales_details', methods=['get'])
@token_required
def get_monthly_sales_details():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if len(auth_header.split()) > 1 else None
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT 
        SUM(m.jumlah) as omzet,
        COUNT(m.nobuk) as jumlah_invoice,
        COUNT(DISTINCT m.kocus) as jumlah_customer
    FROM mso m 
    WHERE m.kosal = '{decoded_token["id"]}' 
    AND EXTRACT(MONTH FROM m.tgl) IN (1) 
    AND EXTRACT(YEAR FROM m.tgl) = 2025;
    """)
    monthly_data=cursor.fetchall()[0]
    output={
        "omzet": monthly_data[0],
        "jumlah_invoice": monthly_data[1],
        "jumlah_customer": monthly_data[2]
    }
    return jsonify(output)


