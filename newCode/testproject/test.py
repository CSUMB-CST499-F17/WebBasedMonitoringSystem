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
# from wallclock import get_time_string_from_unix_time


app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)

#Function to grab css file
def get_resource_as_string(name, charset='utf-8'):
	with app.open_resource(name) as f:
		return f.read().decode(charset)
app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

@app.route('/')
def hello():
	return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
	print "%s USER CONNECTED " %  flask.request.sid

def getData(port,passphrase,hName):
	suiteInformation = authorize(port,passphrase,hName)
	#test variable holds json data
	global json
	global son
	json = suiteInformation.json()
	#print json
	son = suiteInformation.text
	return json



@socketio.on('data')
def authenticate(message):
	link = "http://"+ str(message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
	home = expanduser("~")
	
	passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
	#passphraseFile = home+"/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/two/.service/passphrase"
	global passphrase
	with open(passphraseFile,'r') as f:
		passphrase = f.readline()
	print "PASSPHRASE: ", passphrase
	
	global port
	global hostname

	port = str(message['portNumber'])
	hostname = str(message['hostName'])
	data = getData(port,passphrase,hostname)
	
	host = socket.gethostname()
	# print "SUITE STATUS:", suiteInformation.status_code
	
	#test variable holds json data
	global json
	global son
	json = data.json()
	son = data.text



@app.route('/monitor', methods = ['GET'])
def monitor():

	global port
	global hostname
	global passphrase
	# print json
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
		#print tot
		# print state
		subst = " %d-%s" % (tot,state)
		# print subst
		# summary += get_status_prop(state, 'ascii_ctrl', subst)
		summary += subst
		summer += state
		stateColor.append(state)
		stateValue.append(tot)
	# blit.append(summer)
	print "*******6===================6******************"
	# print blit



	status1 = json[0]['status_string']
	# len_header = sum(len(status1))
	status2 = ''
	suffix = '_'.join(list(status1.replace(' ', '_'))) + status2
	divider_str = '_' * 104
	divider_str = "%s%s" % (
	divider_str[:-len(suffix)], suffix)

	# print divider_str


	print "---------------------------------------------------------"

	task_info = {}
	name_list = set()
	task_ids = other_list.keys()
	for task_id in task_ids:
		# print ("ID: " , task_id)
		name = other_list[task_id]['name']
		# print ("NAME: " , name)
		point_string = other_list[task_id]['label']
		# print ("POINT: " , point_string)
		count += 1
		state = other_list[task_id]['state']
		# print ("STATE: " , state)
		name_list.add(name)
		# print ("LIST: ", name_list)
		# print name
		# print point_string
		# print state
		if point_string not in task_info:
			task_info[point_string] = {}
		task_info[point_string][name] = (state, "color" , name)
		# print task_info
	# print count

	# print "---------------------------------------------------------"


	sorted_name_list = sorted(name_list)
	sorted_task_info = {}
	for point_str, info in task_info.items():
		sorted_task_info[point_str] = collections.OrderedDict()
		# print ("POINT: " , point_str)
		# print ("INFO: " , info)
		for name in sorted_name_list:
			if name in name_list:
				# (Defn order includes family names.).
				# print ("Name666: " ,name)
				# print info.get(name)
				sorted_task_info[point_str][name] = info.get(name)
				# print sorted_task_info
				
	sorted_task_info_2 = sorted(sorted_task_info.items())			

	print "---------------------------------------------------------"

	print update
	print summary
	print divider_str
	tracker = 0
	nameInfo = {}
	labels = []
	labelnames = []
	# print sorted_task_info
	for point_str, val in sorted_task_info_2:
		# print ("POINT: ", point_str)
		# print ("VAL: " , val) 
		indx = point_str
		# print ("INDEX: " ,val)
		line = point_str
		# nameInfo = {}
		labels.append(line)
		# print line
		sline = ""
		for name, info in val.items():
			# print info
			# print ("NAME: " , name)
			# print("I_NFO: ", info)
			if info is not None:
				# tracker += 1
				sline =  " %s" % info[2]
				# labelnames.append(sline)
				# print sline
				# print "we out here"

		# print tracker
		# blitlines[indx] = line
		labelnames.append(sline)
		lineout = "%s: %s" %(line, sline )
		print lineout

	print ""
	print ""
	print ""
	# print labelnames
	# print labels
	#return flask.render_template('monitor.html', son = son, summary = summary, update = update, lineout = lineout, label =zip(labels, labelnames), divider = divider_str, sorted_task_info_2 = sorted_task_info_2, states =zip(stateColor, stateValue) )
	return flask.render_template('monitor.html', response = getData(port,passphrase,hostname), son = son, summary = summary, update = update, lineout = lineout, divider = divider_str, sorted_task_info_2 = sorted_task_info_2, label =zip(labels, labelnames), states =zip(stateColor, stateValue))






if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 # host=socket.gethostname(),
 # debug=True
 )
