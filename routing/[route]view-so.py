from routing import login_required,app,render_template,session,redirect, sqlselect, encrypt, sqlconnect

@app.route('/view_so')
@login_required
def view_so():
    sqlconnection=sqlconnect()
    return render_template('view-so-temp.html',user=session['username'].title(),profile=session['profile'],role=sqlselect(sqlconnection.cursor(),'account', selection='permissions', condition=f"account='{encrypt(session.get('username').upper())}'")[0][0].split(',')[0].title()) 