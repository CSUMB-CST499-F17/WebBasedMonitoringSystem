# test.py
import requests
import collections
import datetime
from time import sleep, time
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

#Returns index page for user input
@app.route('/')
def hello():
	return flask.render_template('index.html')

#when socket connects successfully the data from cylc is grabbed
@socketio.on('connect')
def on_connect():
	print "%s USER CONNECTED " %  flask.request.sid

def getData(port,passphrase,hName):
	suiteInformation = authorize(port,passphrase,hName)
	global json
	global son
	json = suiteInformation.json()
	son = suiteInformation.text
	return json



@socketio.on('data')
def authenticate(message):
	link = "http://"+ str(message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
	home = expanduser("~")
	
	#cylc tutorial suite path to obtain passphrase file
	#need to get generic suite path using suiteName	
	passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
	#passphraseFile = home+"/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/two/.service/passphrase"
	global passphrase
	with open(passphraseFile,'r') as f:
		passphrase = f.readline()
	print "PASSPHRASE: ", passphrase
	
	global port
	global hostname
	global suiteName

	port = str(message['portNumber'])
	hostname = str(message['hostName'])
	suiteName = str(message['suiteName'])
	data = getData(port,passphrase,hostname)
	host = socket.gethostname()

	global json
	global son
	json = data.json()
	son = data.text


#Directs to monitor page, parses all suite data 
@app.route('/monitor', methods = ['GET'])
def monitor():

	global port
	global hostname
	global passphrase
	state_list = json[0]['state totals']
	other_list = json[1]

	#Variables for state summary and update time
	summary = " "
	update = " "
	summer = ""

	#Update variable holds last_updated time from json data
	update_totals = json[0]['last_updated']
	value = datetime.datetime.fromtimestamp(update_totals)
	updated_at = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
	update += updated_at

	ns_defn_order = json[0]['namespace definition order']
	count = 0
	state_totals = json[0]['state totals']

	stateColor = []
	stateValue = []

	for state, tot in state_totals.items():
		subst = " %d-%s" % (tot,state)
		summary += subst
		summer += state
		stateColor.append(state)
		stateValue.append(tot)

	total_tasks = sum(stateValue)


	status1 = json[0]['status_string']
	status2 = ''
	suffix = '_'.join(list(status1.replace(' ', '_'))) + status2
	divider_str = '_' * 104
	divider_str = "%s%s" % (
	divider_str[:-len(suffix)], suffix)


	task_info = {}
	name_list = set()
	task_ids = other_list.keys()
	for task_id in task_ids:
		name = other_list[task_id]['name']
		point_string = other_list[task_id]['label']
		count += 1
		state = other_list[task_id]['state']
		name_list.add(name)

		if point_string not in task_info:
			task_info[point_string] = {}
		task_info[point_string][name] = (state, "color" , name)


	sorted_name_list = sorted(name_list)
	sorted_task_info = {}
	for point_str, info in task_info.items():
		sorted_task_info[point_str] = collections.OrderedDict()
		for name in sorted_name_list:
			if name in name_list:
				sorted_task_info[point_str][name] = info.get(name)
				
				
	sorted_task_info_2 = sorted(sorted_task_info.items())			

	tracker = 0
	nameInfo = {}
	labels = []
	labelnames = []
	
	for point_str, val in sorted_task_info_2:
		indx = point_str
		line = point_str
		labels.append(line)
		sline = ""
		for name, info in val.items():
			if info is not None:
				sline =  " %s" % info[2]
				
		labelnames.append(sline)
		lineout = "%s: %s" %(line, sline )

	return flask.render_template('monitor.html', response = getData(port,passphrase,hostname), summary = summary, update = update, lineout = lineout, divider = divider_str, sorted_task_info_2 = sorted_task_info_2, label =zip(labels, labelnames), states =zip(stateColor, stateValue), total_tasks = total_tasks, suiteName = suiteName)






if __name__ == '__main__':# __name__!

 socketio.run(
 app
 )
