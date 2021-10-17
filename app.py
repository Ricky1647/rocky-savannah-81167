import re
from flask import Flask , template_rendered
from flask.templating import render_template
from flask import url_for
from flask import redirect, request,session
import requests
import urllib.parse
import json
import base64
from pprint import pprint
import os
import hashlib

# クライアント情報
# Channel ID
client_id = "1656533966"
# Channel Secret
client_secret = "89af3c3c3010bf8d182d4a1e88edb7b9"
# Callback URL
redirect_uri = 'https://rocky-savannah-81167.herokuapp.com/callback'
# LINE エンドポイント
authorization_url = 'https://access.line.me/dialog/oauth/weblogin'
token_url = 'https://api.line.me/v2/oauth/accessToken'
user_info_url = 'https://api.line.me/v2/profile'


app = Flask(__name__)
app.secret_key = 'session_key'


@app.route("/")
def login():
    # ステート生成
    state = hashlib.sha256(os.urandom(32)).hexdigest()
    #state = "login"
    session['state'] = state
    # 認可リクエスト
    return redirect(authorization_url+'?{}'.format(urllib.parse.urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
        'response_type': 'code'
    })))

@app.route("/callback")
def callback():
    # 2. ユーザー認証/同意を行い、認可レスポンスを受け取る。
    # 認可コードを受け取る:https://developers.line.biz/ja/docs/line-login/integrate-line-login-v2/#receiving-the-authorization-code
    state = request.args.get('state')
    if state != session['state']:
         print("invalid_redirect")
    code = request.args.get('code')
    print(code)
    print("1saaas")
    # 3. 認可レスポンスを使ってトークンリクエストを行う。
    # ウェブアプリでアクセストークンを取得する:https://developers.line.biz/ja/docs/line-login/integrate-line-login-v2/#get-access-token
    body = urllib.parse.urlencode({
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }).encode('utf-8')
    req, res = '', ''
    req = urllib.request.Request(token_url)
    with urllib.request.urlopen(req, data=body) as f:
        res = f.read()
    access_token = json.loads(res)['access_token']
    # 4. 取得したアクセストークンを使用してユーザープロフィールを取得する。
    # ユーザープロフィールを取得する:https://developers.line.biz/ja/docs/line-login/managing-users/#get-profile
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    req = urllib.request.Request(user_info_url, headers=headers, method='GET')
    with urllib.request.urlopen(req) as f:
        res = f.read()
    # with open('token.json', 'w') as f:
    #     json.dump(res, f)
    #return render_template("index.html")
    return json.loads(res)



# @app.route("/",methods= ["GET","POST"])
# def main():
#     r = requests.get('https://api.line.me/v2/oauth/accessToken')
#     print(r)
#     print("dd")
#     return render_template("login.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return redirect(url_for('index'))
#     return render_template("login.html")

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True) 