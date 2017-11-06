# app.py
import requests
import os, flask, flask_socketio,requests
from flask_socketio import emit,send
import json
from flask import jsonify
from requests.auth import HTTPDigestAuth
import socket
from os.path import expanduser
from au import authorize

app = flask.Flask(__name__)


socketio = flask_socketio.SocketIO(app)


@app.route('/')
def hello():
	return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
	print "%s USER CONNECTED " %  flask.request.sid


@socketio.on('data')
def message(message):

	print "%s IS HOST NAME " % message['hostName']
	print "%s IS PORT NUMBER " % message['portNumber']
	print "%s IS SUITE NAME " % message['suiteName']
	link = "http://"+ str( message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
 #Verify not necessary: TODO: Verify = FALSE should not skip authentication.
 #10/24 open passphrase file
 #example suites are a different path because it creates example folder for all
 	#suiteName = str(message["suiteName"])
	home = expanduser("~")
#typical non-example suite path
	#passphraseFile = home+"/cylc-run/"+suiteName+"/.service/passphrase
	
 	passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
#get passphrase from file as a string pass as second argument to HTTPDigestAuth
	with open(passphraseFile,'r') as f:
   		passphrase = f.readline()
 	print "PASSPHRASE: ", passphrase
	
	 

	suiteInformation = authorize(str(message['portNumber']),passphrase,str(message['hostName']))
	#print "SUITE STATUS:", suiteInformation.status_code
	#print suiteInformation.json()
	#print suiteInformation.text
	


if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 host=socket.gethostname(),
 debug=True
 )
