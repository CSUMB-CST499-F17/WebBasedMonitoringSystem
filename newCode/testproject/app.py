# app.py
import requests
from time import sleep, time
from status import (
    TASK_STATUS_RUNAHEAD, TASK_STATUSES_ORDERED,
    TASK_STATUSES_RESTRICTED)
import os, flask, flask_socketio,requests
from flask_socketio import emit,send
import json
from flask import jsonify
from requests.auth import HTTPDigestAuth
import socket
from os.path import expanduser
from au import authorize
from flask import Flask, request, url_for, redirect
# from wallclock import get_time_string_from_unix_time


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
# @app.route('/monitor', methods = {'GET', 'POST'})
# #@app.route('/monitor', )
# def monitor():
#     return flask.render_template('monitor.html', test = test, dat = dat, moredat = moredat)


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
	print suiteInformation.json()
	print suiteInformation.text
	
	#test variable holds json data
	global test
	test = suiteInformation.json()

	global dat
	global summary
	global updated
	global task_summaries
	blit = []
    
	# dat = test[0]['state totals']['ready']
	dat = test[0]
	time = test[0]
	task_summaries = test[0]



	summary = 'state summary:'
	update_totals = dat['last_updated']
   	state_totals = dat['state totals']
   	updated = update_totals
   	print updated

   	# update_totals = dat['last_updated']
	# updated= "updated: \033[1;38m%s\033[0m" % update_totals
	
   	for state, tot in state_totals.items():
   		#print tot
   		# print state
		subst = " %d " % tot
		print subst
	    # summary += get_status_prop(state, 'ascii_ctrl', subst)
	   	summary += subst
	   	# summary += tot

   	blit.append(summary)

   	  	# task_summaries = dict(
    # 	(i, j) for i, j in task_summaries.items() 
    # 		if (j['state'] != TASK_STATUS_RUNAHEAD))


   	print '\n'.join(blit)


	# global test
	# test = suiteInformation.json()
	# print test
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	# global dat
	# dat = test[0]['state totals']['ready']
	#dat = test[2]
	print dat
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	global moredat
	moredat = test[2]
	# print moredat
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	# print dat


#@app.route('/monitor', methods = {'GET', 'POST'})
@app.route('/monitor')
def monitor():
    return flask.render_template('monitor.html', test = test, summary = summary, updated = updated, moredat = moredat)





if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 # host=socket.gethostname(),
 # debug=True
 )
