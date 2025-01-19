from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os
from datetime import datetime, timedelta, timezone
SECRET_KEY = os.getenv("SECRET_KEY")
@app.route('/api/v1/sales/get_so', methods=['get'])
@token_required
def get_so():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if len(auth_header.split()) > 1 else None
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT
        m.nobuk,
        m.namcus,
        m.jumlah,
        m.tgl,
        m.jtempo,
        m.kosal,
        ksl.namsal,
        count(mu.kobar) as items
        FROM
        mso m
    LEFT JOIN kosal ksl ON m.kosal = ksl.kosal
    LEFT JOIN mutso mu ON mu.nobuk = m.nobuk
    WHERE m.kosal = '{decoded_token["id"]}'
    GROUP BY
        m.nobuk,
        m.jumlah,
        m.namcus,
        m.tgl,
        m.jtempo,
        m.kosal,
        ksl.namsal
    order by m.tgl desc
    ROWS {1} TO {1+29}
        """)
    so_data=cursor.fetchall()
    return jsonify(so_data)
