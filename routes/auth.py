from flask import request, Response
from functools import wraps
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/users.json")

def load_users():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def check_auth(username, password):
    users = load_users()
    return username in users and users[username] == password

def authenticate():
    return Response("Authentication required", 401,
                    {"WWW-Authenticate": 'Basic realm="Login Required"'})

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
