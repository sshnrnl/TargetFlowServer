from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/v1/sales/get_stock', methods=['get'])
def get_stock_list():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""SELECT b.KoBar, b.NamBar, b.KoKel, b.NamKel, (b.Qty / COALESCE(t.Kvrsi, 1)) SisaStok, COALESCE(t.KoSat, b.KoSat) KoSat FROM YKS_SISASTOK('TBKOBAR.KoGud = ''GDG''') b LEFT OUTER JOIN TBKVRSI t ON (b.KoBar=t.KoBar)""")
    a=cursor.fetchall()

    return jsonify(
        items=a,
        items_count=len(a),
        emergency_stock=len([i for i in a if i[4] < 10 and i[4] > 0]),
        stock_critical=len([i for i in a if i[4] == 0])
    )