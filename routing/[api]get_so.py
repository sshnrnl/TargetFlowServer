from datetime import timedelta
from routing import login_required,app,render_template,session,select,select_range,request,jsonify,connect

@app.route('/api/marketing/get_so', methods=['post'])
def get_so():
    content = request.json
    start=content['data']+1
    qty=request.args.get('qty')
    additional={}
    if not qty:qty=10
    connection=connect()
    cursor=connection.cursor()
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
    GROUP BY
        m.nobuk,
        m.jumlah,
        m.namcus,
        m.tgl,
        m.jtempo,
        m.kosal,
        ksl.namsal
    order by m.tgl desc
    ROWS {start} TO {start+29}
        """)
    so_data=cursor.fetchall()
    for i in so_data:
        additional[i[0]]=['']
        additional[i[0]][0]=i[3]+timedelta(days=i[4])
    # print(additional)
    return jsonify({"data":so_data, 'additional':additional})

@app.route('/api/marketing/get_specific_so', methods=['post'])
@login_required
def get_specific_so():
    content = request.json
    soID=content['soID']
    print(soID)
    connection=connect()
    cursor=connection.cursor()
    cursor.execute(f"""
    SELECT
        m.namcus,
        m.nobuk,
        ksl.namsal,
        m.jtempo,
        m.tgl,
        m.jumlah
    FROM mso m
    LEFT JOIN kosal ksl ON m.kosal = ksl.kosal
    where m.nobuk='{soID}'
    order by m.tgl desc
    """)
    soData=cursor.fetchall()
    cursor.execute(f"""
    SELECT
        kb.nambar || ' (' || mu.satqty || ')',
        mu.qty,
        mu.satqty,
        mu.kvrsiqty,
        mu.harga,
        mu.sathrg,
        mu.kvrsihrg,
        (mu.kvrsiqty*mu.harga) as rill,
        mu.jumlah
    FROM mso m
    LEFT JOIN mutso mu using(nobuk)
    LEFT JOIN kobar kb on mu.kobar=kb.kobar
    where m.nobuk='{soID}'
    """)
    items=cursor.fetchall()
    print(items)
    # print(soData)
    return jsonify({"data": soData, "items":items})