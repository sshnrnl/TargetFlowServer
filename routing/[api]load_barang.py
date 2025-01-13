from routing import login_required,app,render_template,session,select, select_range,request,jsonify,connect

@app.route('/api/sales/load_barang', methods=['post'])
def load_barang():
    connection=connect()
    a=select(tables="kobar", connect=connection, selection="nambar, kobar", order='nambar')

    return jsonify(a)
