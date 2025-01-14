from api.index import app, sqlconnect, sqlselect

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    conn =sqlconnect()
    curr =conn.cursor()
    a=sqlselect(cursor=curr, tables="users")
    return a