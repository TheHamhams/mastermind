from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

def secret_key_required(flask_function):
    @wraps(flask_function)

    def decorated(*args, **kwargs):
        current_secret_key = None

        if 'x-access-token' in request.headers:
            current_secret_key = request.headers['x-access-token'].split(' ')[1]
            print(current_secret_key)
            print(SECRET_KEY)
        if not current_secret_key:
            return jsonify({'message': 'Access key is missing'}), 401

        if current_secret_key != SECRET_KEY:
            return jsonify({'message': 'Invalid access key'})

        return flask_function(current_secret_key, *args, **kwargs)

    return decorated