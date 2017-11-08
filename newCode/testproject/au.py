#au.py
#Function is called in app.py for authorization
import requests

def authorize(portNumber,passphrase,hostName):
	# hostName = 'localhost'
	url = "http://%s:%s/state/get_state_summary" % (hostName,portNumber)
	auth = requests.auth.HTTPDigestAuth('cylc', passphrase)
	session = requests.Session()

	ret = session.get(
                    url,
                    auth=auth
                )

	return ret
