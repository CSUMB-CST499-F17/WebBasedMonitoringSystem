#au.py
#needs incorporated with new app.py
import requests
from os.path import expanduser

hostName = 'localhost'
portNumber = 43083
home = expanduser("~")
#typical non-example suite path
#passphraseFile = home+"/cylc-run/"+suiteName+"/.service/passphrase
#passphraseFile = home+"/cylc-run/examples/7.5.0/tutorial/cycling/one/.service/passphrase"
passphraseFile = home+"/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/one/.service/passphrase"
with open(passphraseFile,'r') as f:
   	passphrase = f.readline()
url = "http://%s:%d/state/get_state_summary" % (hostName,portNumber)
auth = requests.auth.HTTPDigestAuth('cylc', passphrase)
session = requests.Session()



def _get_verify():
    """Return the server certificate if possible."""
    return server_cert = home + "/cylc-run/tmp/cylc-examples/7.5.0/tutorial/cycling/one/.service/ssl_cert"


ret = session.get(
                    url,
                    auth=auth,
                    verify=_get_verify()
                )

print ret.status_code
print ret.json()
print ret.text
