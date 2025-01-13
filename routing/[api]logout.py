from routing import app, login_required,session,redirect,url_for

@app.route('/logout')
@login_required
def logout():
    session['username']=None
    session['permissions']=None
    session['profile']=None
    return redirect(url_for('login'))