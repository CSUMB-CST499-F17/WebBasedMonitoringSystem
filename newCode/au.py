
#au.py
import requests
from os.path import expanduser

hostName = 'localhost'
portNumber = 4005
home = expanduser("~")
#typical non-example suite path
#passphraseFile = home+"/cylc-run/"+suiteName+"/.service/passphrase
passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
with open(passphraseFile,'r') as f:
   	passphrase = f.readline()
url = "http://%s:%d/state/get_state_summary" % (hostName,portNumber)
auth = requests.auth.HTTPDigestAuth('cylc', passphrase)
session = requests.Session()

ret = session.get(
                    url,
                    auth=auth
                )

print ret.status_code
print ret.json()
print ret.text
