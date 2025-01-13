from routing import sqlcommit,sqlinsert,login_required,app,render_template,session,select, select_range,request,jsonify,connect, sqlconnect, sqlselect

@app.route('/api/admin/insert_target', methods=['post'])
def insert_target():
    content = request.json
    temp_start_date=content['start'].strip()[0:10].split('-')
    temp_end_date=content['end'].strip()[0:10].split('-')
    
    start_date='-'.join(temp_start_date[::-1])+" "+content['start'].strip()[-5::]
    
    end_date='-'.join(temp_end_date[::-1])+" "+content['end'].strip()[-5::]
    connection = sqlconnect()
    target_number=sqlselect(connection.cursor(), 'target',selection='COUNT(*)')[0][0]+1
    print(content)
    sqlinsert(connection.cursor(), tables='target', values=f"{target_number}, '{start_date}', '{end_date}', {1}")
    sqlcommit(connection)
    # for i in content['items']:
    #     print(i, content[i])
    return jsonify({"data":"adsf"})