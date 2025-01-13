#############################################
#                                           #
#               login_attempt               #
#                                           #
#  Author: Shan                             #
#                                           #
#############################################
#                                           #
#  Post Request untuk memvalidasi akun      #
#                                           #
#############################################

from routing import app, encrypt, request, sqlconnect, session,sqlselect,url_for,jsonify

@app.route('/api/login_attempt', methods=['post'])
def login_attempt():
    content = request.json
    username = encrypt(content['username'].upper())
    password = encrypt(content['password'])
    print(username,password)
    connection=sqlconnect()
    cursor=connection.cursor()
    if(int(sqlselect(cursor,'account', selection=f"count(*)", condition=f"account='{username}' and password='{password}'")[0][0])>=1):
        print("Logged in")
        session['username']=content['username']
        session['profile']=sqlselect(cursor,'account', selection=f"profile", condition=f"account='{username}' and password='{password}'")[0][0]
        return jsonify({"url":url_for('view_so')})
    else:raise Exception("Akun tidak valid")