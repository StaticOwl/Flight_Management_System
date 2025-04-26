from functools import wraps

import jwt
from flask import request, jsonify

# Use the same secret key that's used in your controllers.py
SECRET_KEY = ''

def role_required(roles):
    """
    Decorator to check if user has the required role(s)
    
    Args:
        roles (list or str): A list of allowed roles or a single role string
    
    Returns:
        The decorated function if user has the required role, error response otherwise
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Check if the authorization header exists
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'message': 'Token is malformed!'}), 401
            
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            
            try:
                # Decode the token
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_role = data.get('role', 'customer')  # Default to 'customer' if no role found
                
                # Convert single role to list for consistent checking
                allowed_roles = roles if isinstance(roles, list) else [roles]
                
                # Check if user has one of the allowed roles
                if current_role not in allowed_roles:
                    return jsonify({'message': 'Permission denied. Required role(s): ' + ', '.join(allowed_roles)}), 403
                
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401
            except Exception as e:
                return jsonify({'message': f'Error processing token: {str(e)}'}), 500
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator