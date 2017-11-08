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
from flask import Flask, request, url_for, redirect


app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)

#Function to grab css file
def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)
app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

@app.route('/', methods = {'GET', 'POST'})
def hello():
	return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
	print "%s USER CONNECTED " %  flask.request.sid

#Opens the cylc monitor webpage
@app.route('/', methods = {'GET', 'POST'})
@app.route('/monitor', )
def monitor():
    return flask.render_template('monitor.html', test = test, dat = dat, moredat = moredat)


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
	
 	# passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
 	passphraseFile = home+"/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/one/.service/passphrase"
#get passphrase from file as a string pass as second argument to HTTPDigestAuth
	with open(passphraseFile,'r') as f:
   		passphrase = f.readline()
 	print "PASSPHRASE: ", passphrase
	
	suiteInformation = authorize(str(message['portNumber']),passphrase,str(message['hostName']))
	host = socket.gethostname()
	# print "SUITE STATUS:", suiteInformation.status_code
	# print suiteInformation.json()
	# print suiteInformation.text
	
	global test
	# test = suiteInformation.json()
	test = suiteInformation.text
	
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	global dat
	# dat = test[0]['state totals']['ready']
	dat = test[2]
	print dat
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	global moredat
	moredat = test[2]
	# print moredat
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	# print dat

if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 # host=socket.gethostname(),
 # debug=True
 )
