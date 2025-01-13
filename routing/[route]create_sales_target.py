from routing import login_required,app,render_template,session, select, connect

@app.route('/admin/create_sales_target')
# @login_required
def create_sales_target():
    connection=connect()
    return render_template('create_sales_target.html') 
    # return render_template('index.html',username=session['username']) 