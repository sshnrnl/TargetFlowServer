from api.index import app, db, jwt, request, jsonify, token_required
from api.database_model import User  # Make sure User is imported

@app.route('/api/v1/sales/get_sales', methods=['GET'])  # use uppercase 'GET'
def get_sales():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })

    return jsonify(result), 200
