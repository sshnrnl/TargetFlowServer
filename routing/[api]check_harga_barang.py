from routing import login_required,app,render_template,session,select, select_range,request,jsonify,connect

@app.route('/api/sales/check_harga', methods=['post'])
def load_harga():
    content = request.json
    kobar=content['kobar']
    connection=connect()
    a=select(tables="kobar", connect=connection, selection="*", order='nambar', condition=f"kobar='{kobar}'")[3]
    return jsonify(a)