import re
from flask import Flask , template_rendered
from flask.templating import render_template
from flask import url_for
from flask import redirect, request
import requests

access_token = 'C..='
userId = 'U..d'

app = Flask(__name__)

@app.route("/",methods= ["GET","POST"])
def main():
    r = requests.get('https://api.line.me/v2/oauth/accessToken')
    print(r)
    print("dd")
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True) 