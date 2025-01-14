from api.index import app, sqlconnect, sqlselect
import jwt  # Import PyJWT for handling JWT tokens
from flask import request, jsonify
import os
from datetime import datetime, timedelta, timezone

# Load the secret key from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/login', methods=["POST"])
def login():
    try:
        # Get user credentials from the request body
        user_data = request.json
        username = user_data.get('username')
        password = user_data.get('password')

        # Establish database connection and fetch user details
        conn = sqlconnect()
        curr = conn.cursor()
        
        # Query the database for the user with the provided username and password
        user = sqlselect(curr, "users", condition=f"username='{username}' AND password='{password}'")
        
        # If the user does not exist or the credentials are incorrect
        if not user:
            return jsonify({"message": "Invalid username or password"}), 401
        
        # If the user exists, generate a JWT token
        payload = {
            'sub': username,  # Subject of the token (typically the username or user ID)
            'iat': datetime.now(timezone.utc),  # Issued at time (current time, timezone-aware)
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # Expiration time (1 hour from now)
        }
        
        # Encode the token using the secret key
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        # Return the token as a response
        return jsonify({
            "message": "Login successful",
            "access_token": token
        })
    
    except Exception as e:
        # If any error occurs, return the error message
        return jsonify({"message": str(e)}), 500
