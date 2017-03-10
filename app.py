# app.py
import os, flask, flask_socketio,requests
from flask_socketio import emit,send
import json

app = flask.Flask(__name__)



socketio = flask_socketio.SocketIO(app)



@app.route('/')
def hello():
 return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
 print "%s USER CONNECTED " %  flask.request.sid
@socketio.on('data')
def bot_message(message):
 emit ('summary_info',message)
  
@socketio.on('disconnect')
def on_disconnect():
 print "USER DISCONNECTED"
 
    
if __name__ == '__main__':# __name__!

 socketio.run(
 app,
 debug=True
 )
