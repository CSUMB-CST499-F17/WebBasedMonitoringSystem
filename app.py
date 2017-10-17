# app.py
import os, flask, flask_socketio,requests
from flask_socketio import emit,send
import json
from flask import jsonify
from requests.auth import HTTPDigestAuth
import socket

#imports to use flask-login
from flask_login import LoginManager, login_user, login_required, logout_user

#imports for database and password encryption
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = flask.Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)

#database and bcrypt
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.sqlite3'
app.config['SECRET_KEY'] = "\xb6\x13\x14g'\x10A\xec\x1e\x1a\x110*\xd0\xfe\x8d\x9a\x80-QG$\xdb\xad"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


socketio = flask_socketio.SocketIO(app)



@app.route('/')
def hello():
 return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
 print "%s USER CONNECTED " %  flask.request.sid


@socketio.on('data')
def message(message):
 app.logger.warning('A warning occurred (%d apples)', 42)
 app.logger.error('An error occurred')
 app.logger.info('Info')
# print message
# print message["hostName"]
 link = "http://"+ str( message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
 #Verify not necessary: TODO: Verify = FALSE should not skip authentication.
 r=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'))
 data = r.json()
 try:
    link2 = "http://" + str( message["hostName"]) + ":" + str(message["portNumber"]) + '/info/get_graph_raw?stop_point_string=' + data[0]["newest cycle point string"] + '&ungroup_recursive=False&start_point_string='+data[0]["oldest cycle point string"]+'&group_nodes=None&ungroup_nodes=None&ungroup_all=False&group_all=True'
    r2=requests.get(link2,auth=HTTPDigestAuth('anon','the quick brown fox'))
    data.append(r2.json())
 except:
    print "Empty list"
 #grab name from other cylc endpoint
 link = "http://"+ str(message["hostName"]) + ":"+str(message["portNumber"]) + '/id/identify'
 r=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'))
 name=r.json()
 data.append({"name":name["name"]})
 print json.dumps(data,indent=2)
 emit ('summary_info',data)

@socketio.on('localData')
def local(message):
 app.logger.warning('A warning occurred (%d apples)', 42)
 app.logger.error('An error occurred')
 app.logger.info('Info')
# print message
# print message["hostName"]
#TODO:wrap in try catch so server doesn't crash
 link = "http://"+ str(socket.gethostname()) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
 #Verify not necessary: TODO: Verify = FALSE should not skip authentication.
 r=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'))
 data = r.json()
 emit ('summary_info',data)
@socketio.on('disconnect')
def on_disconnect():
 print "USER DISCONNECTED"


@socketio.on('getName')
def name(message):
 # print message
# print message["hostName"]
 portNumber=43000
 r=["Error in request"]
 print r[0]
 #check all ports that cylc searches through by default
 while portNumber<43101:
 	link = "http://"+ str(socket.gethostname()) + ":"+str(portNumber) + '/id/identify'
 #Verify not necessary: TODO: Verify = FALSE should not skip authentication.
        portNumber=portNumber+1
 	try:
		 r=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'))
		 r=r.json()
		 print json.dumps(r,indent=2)
                 print r["name"]
		 print message
                 print portNumber
                 if message["suiteName"] in r["name"]:
                        portNumber=portNumber-1
			break
 	except requests.ConnectionError, e:
		print e
        	r=["Error in request"]


 #print json.dumps(data,indent=2)
 emit ('name',{"name":r["name"],"portNumber":portNumber})



@socketio.on('stop_suite')
def stop_suite(message):
    stop_link = "https://"+ str( message["hostName"]) + ":" + str(message["portNumber"]) + '/state/get_state_summary'
    stopped_task=requests.get(link,auth=HTTPDigestAuth('anon','the quick brown fox'), verify=False)



if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 host=socket.gethostname(),
 debug=True
 )
