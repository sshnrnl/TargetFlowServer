from routing import app, logout_required,render_template

@app.route('/login')
@logout_required
def login():
    return render_template('login.html')