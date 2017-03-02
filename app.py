from flask import Flask
import requests
import json
from requests.auth import HTTPDigestAuth
app = Flask(__name__)

@app.route("/")
def hello():
    headers={
    'username':'anon',
    'password':'the quick brown fox'
    }
    link='http://brandan-virtualbox:43029/id/identify'
    r=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'))
    print r.text
    return r.text

if __name__ == "__main__":
    app.run()
