from functools import wraps
from flask import request, jsonify
import jwt
from main.__init__ import app

SECRET_KEY = '' 

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
                
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
                
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_role = data['role']
                
                if current_role not in roles:
                    return jsonify({'message': 'Permission denied!'}), 403
                
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator