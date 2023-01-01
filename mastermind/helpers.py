from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

def secret_key_required(flask_function):
    '''
    Require the secret key to be sent to authorize admin api routes
    '''
    @wraps(flask_function)

    def decorated(*args, **kwargs):
        current_secret_key = None

        if 'x-access-token' in request.headers:
            current_secret_key = request.headers['x-access-token'].split(' ')[1]

        # Check if secret key was sent
        if not current_secret_key:
            return jsonify({'message': 'Access key is missing'}), 401

        # Check if sent secret key matches the secret key
        if current_secret_key != SECRET_KEY:
            return jsonify({'message': 'Invalid access key'})

        return flask_function(current_secret_key, *args, **kwargs)

    return decorated