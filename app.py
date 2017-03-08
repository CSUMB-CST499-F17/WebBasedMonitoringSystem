from flask import Flask
from flask import request
from flask import jsonify, render_template
import requests
import json
from requests.auth import HTTPDigestAuth
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data", methods=['POST'])
def values():

    if request.method == 'POST':
        
        #Get the values from html template.
        host_name = request.form['hostName']
        port_number = request.form['portNumber'] 

        
        #TODO: Link is hard typed for now.
        link = "https://" + host_name + ":" + str(port_number) + '/id/identify'

        #Verify not necessary: TODO: Verify = FALSE should not skip authentication.
        r=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'), verify=False)
        data = r.json()
        print data

        #Send data to template.
        return render_template("index.html", data=data)
        
if __name__ == "__main__":
    app.debug = True
    app.run()
