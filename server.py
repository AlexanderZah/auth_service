
from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response

import hmac
from hashlib import sha256
import json
from typing import Optional
import base64


app = FastAPI()

SECRET_KEY = '1653811ef8dc892d874ba00e0be06eec2c65750aa1c5d14c5501093bb0da5fc7'
PASSWORD_SALT = 'b20b975f06ee429f05402c8fd8942c\
363ef7bbfe0dc03b55deeead3f666996df'


def sign_data(data: str) -> str:
    """Возвращает подписанные данные data"""
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=sha256
    ).hexdigest().upper()


def get_username_from_signed_data(username_signed: str) -> Optional[str]:

    username_base64, sign = username_signed.split('.')
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


def verify_password(password: str, password_hash: str) -> bool:
    stored_password_hash = sha256((
        password + PASSWORD_SALT
        ).encode()).hexdigest()

    return stored_password_hash == password_hash


users = {
    'vasya@user.com': {
        'name': 'Vasya',
        'password': '0aea0029beb6781e11db1e24ecdd48b1\
f932b5a35eb8863ef0714cde6806de0f',
        'balance': 100_000,
    },
    'petr@user.com': {
        'name': 'Petr',
        'password': '6317c81187a083c6fa1c2f3043b36ae0c424d03\
567d40f039b257401cc8637b5',
        'balance': 555_555,
    },
}


@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('./templates/login.html', 'r') as login:
        login_html = login.read()

    if not username:
        return Response(
            login_html, media_type='text/html'
        )

    valid_username = get_username_from_signed_data(username)
    if not valid_username:
        response = Response(
            login_html, media_type='text/html'
        )
        response.delete_cookie(key='username')
        return response

    user = users.get(valid_username)
    if user is None:
        response = Response(
            login_html, media_type='text/html'
        )
        response.delete_cookie(key='username')
        return response

    return Response(
        f'Hello, {users[valid_username]["name"]} !',
        media_type='text/html'
    )


@app.post('/login')
def process_login_page(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)

    if not user or not verify_password(password, user['password']):
        return Response(
            json.dumps({
                'success': False,
                'message': 'Я вас не знаю!!!'
            }),
            media_type='application/json'
        )

    responce = Response(
        json.dumps({
            'success': True,
            'message': f'Привет, {user["name"]}!\
<br /> Твой баланс: {user["balance"]}',
        }),
        media_type='application/json'
    )

    username_signed = base64.b64encode(username.encode()).decode() + '.' \
        + sign_data(username)
    responce.set_cookie(key='username', value=username_signed)

    return responce
