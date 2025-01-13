from routing import login_required,app,render_template,session,select,request,jsonify,connect

@app.route('/api/sales/load_customer', methods=['post'])
@login_required
def load_customer():
    connection=connect()
    a=select(tables="kocus", connect=connection, selection="namcus, kocus", order='namcus')
    return jsonify(a)