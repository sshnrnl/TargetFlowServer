import jwt # type: ignore
from functools import wraps
from flask import request, jsonify # type: ignore
import os
# Secret key used for encoding/decoding the JWT
SECRET_KEY = os.getenv("SECRET_KEY")

def decode_token():
    tkn = request.headers.get('Authorization')
    if not tkn:
            return jsonify({"message": "Authorization header missing"}), 401
        
        # Pisahin Token dari 'Bearer'
    tkn = tkn.split(" ")[1] if len(tkn.split()) > 1 else None
    if not tkn:
        return jsonify({"message": "Authorization header missing"}), 401
    try:
        # Decode the JWT token using the secret key and HS256 algorithm
        decoded_token = jwt.decode(tkn, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    

# Decorator validasi JWT
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Ekstrak Token Dari Header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"message": "Authorization header missing"}), 401
        
        # Pisahin Token dari 'Bearer'
        token = auth_header.split(" ")[1] if len(auth_header.split()) > 1 else None
        
        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            # Validasi jwt
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        # Add user info ke request
        request.user = decoded_token
        
        # Origin Function
        return f(*args, **kwargs)

    return decorated_function
