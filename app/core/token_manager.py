# app/core/token_manager.py
token = None

def set_token(new_token: str):
    global token
    token = new_token

def get_token():
    return token
