from routing import encrypt,login_required,app,render_template,session, permissions,sqlselect, sqlconnect

@app.route('/create_sales_order')
@login_required
def create_sales_order():
    connection=sqlconnect()
    return render_template('create_sales_order.html',user=session['username'].title(),sales_name=session['username'].upper(),profile=session['profile'],role=sqlselect(connection.cursor(),'account', selection='permissions', condition=f"account='{encrypt(session.get('username').upper())}'")[0][0].split(',')[0].title() ) 