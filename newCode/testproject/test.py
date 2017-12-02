# app.py
import requests
import collections
import datetime
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

@app.route('/')
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


# @socketio.on('data')
# def message(message):

# 	print "%s IS HOST NAME " % message['hostName']
# 	print "%s IS PORT NUMBER " % message['portNumber']
# 	print "%s IS SUITE NAME " % message['suiteName']
# 	link = "http://"+ str( message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
#  #Verify not necessary: TODO: Verify = FALSE should not skip authentication.
#  #10/24 open passphrase file
#  #example suites are a different path because it creates example folder for all
#  	#suiteName = str(message["suiteName"])
# 	home = expanduser("~")
# #typical non-example suite path
# 	#passphraseFile = home+"/cylc-run/"+suiteName+"/.service/passphrase
	
#  	# passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
#  	passphraseFile = home+"/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/one/.service/passphrase"
# #get passphrase from file as a string pass as second argument to HTTPDigestAuth
# 	with open(passphraseFile,'r') as f:
#    		passphrase = f.readline()
#  	print "PASSPHRASE: ", passphrase
	
# 	suiteInformation = authorize(str(message['portNumber']),passphrase,str(message['hostName']))
# 	host = socket.gethostname()
# 	# print "SUITE STATUS:", suiteInformation.status_code
# 	print suiteInformation.json()
# 	print suiteInformation.text
	
# 	#test variable holds json data
# 	global test
# 	test = suiteInformation.json()

# 	global dat
# 	global summary
# 	global updated
# 	global task_summaries
# 	blit = []
	
# 	# dat = test[0]['state totals']['ready']
# 	dat = test[0]
# 	time = test[0]
# 	task_summaries = test[0]



# 	summary = ''
# 	update_totals = dat['last_updated']
#    	state_totals = dat['state totals']
#    	value = datetime.datetime.fromtimestamp(update_totals)
# 	updated = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
#    	print updated

#    	# update_totals = dat['last_updated']
# 	# updated= "updated: \033[1;38m%s\033[0m" % update_totals
	
#    	for state, tot in state_totals.items():
#    		#print tot
#    		# print state
# 		subst = " %d-%s " % (tot,state)
# 		print subst
# 	    # summary += get_status_prop(state, 'ascii_ctrl', subst)
# 	   	summary += subst
# 	   	# summary += tot

#    	blit.append(summary)

#    	  	# task_summaries = dict(
#     # 	(i, j) for i, j in task_summaries.items() 
#     # 		if (j['state'] != TASK_STATUS_RUNAHEAD))


#    	print '\n'.join(blit)


# 	# global test
# 	# test = suiteInformation.json()
# 	# print test
# 	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
# 	# global dat
# 	# dat = test[0]['state totals']['ready']
# 	#dat = test[2]
# 	print dat
# 	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
# 	global moredat
# 	moredat = test[2]
# 	# print moredat
# 	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
# 	# print dat





@socketio.on('data')
def authenticate(message):
	link = "http://"+ str( message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
	home = expanduser("~")
	
	# passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
	passphraseFile = home+"/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/two/.service/passphrase"
	#get passphrase from file as a string pass as second argument to HTTPDigestAuth
	with open(passphraseFile,'r') as f:
		passphrase = f.readline()
	print "PASSPHRASE: ", passphrase
	
	suiteInformation = authorize(str(message['portNumber']),passphrase,str(message['hostName']))
	host = socket.gethostname()
	# print "SUITE STATUS:", suiteInformation.status_code
	# print suiteInformation.json()
	# print suiteInformation.text
	
	#test variable holds json data
	global json
	# global son
	json = suiteInformation.json()
	print json
	# son = suiteInformation.text



@app.route('/monitor', methods = ['GET'])
def monitor():
	# print json
	state_list = json[0]['state totals']
	other_list = json[1]

	#Variables for state summary and update time
	summary = " "
	update = " "
	# summer = ""

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
		# summer += state
		stateColor.append(state)
		stateValue.append(tot)
	# blit.append(summer)
	print "*******6===================6******************"
	# print blit
	total_tasks = sum(stateValue)




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
	# print ("NAME LIST" , name_list)
	# print ("SORTED NAME LIST" , sorted_name_list)
	# print point_string
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
	# print  sorted_task_info_2
	# sorted_task_info_2 = {}
	# for key, value in sorted(sorted_task_info.items()):
	# 	# print ("Sorted SHIT: " , (key, sorted_task_info[key]))
	# 	print "KEY: "
	# 	print key
	# 	# sorted_task_info_2[key] = {}
	# 	if key not in sorted_task_info_2:
	# 		sorted_task_info_2[key] = {}
	# 		print "Just HOllaaaaa!"
	# 		print sorted_task_info_2[key]
	# 	sorted_task_info_2[key] = value
	# 	print "VALUE: "
	# 	print value
	# 	print "DICT: "
	# 	print sorted_task_info_2[key]
	# # 	# sorted_task_info_2[key] = sorted_task_info[key]
	# # 	# temp = sorted_task_info[key]
	# # 	# sorted_task_info_2.update(temp) 
	# # 	temp = {}
	# # 	# temp[key] = value
	# # 	# sorted_task_info_2.update(temp)
	# # 	if value is not None:
	# # 		temp[key] = value
	# # 	sorted_task_info_2.update(temp)
	# # 	# for name, info in value.items():
	# # 		# sorted_task_info_2[key] = info
	# # # print temp
	# # print sorted_task_info_2	


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
	return flask.render_template('monitor.html', total_tasks = total_tasks, summary = summary, update = update, lineout = lineout, label =zip(labels, labelnames), divider = divider_str, sorted_task_info_2 = sorted_task_info_2, states =zip(stateColor, stateValue) )






#@app.route('/monitor', methods = {'GET', 'POST'})
# @app.route('/monitor')
# def monitor():
#     return flask.render_template('monitor.html', summary = summary, updated = updated)





if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 # host=socket.gethostname(),
 # debug=True
 )
