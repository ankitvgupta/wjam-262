""" 
server.py
This is the main driver program for the backend server. 

This should be run by selecting the appropriate transfer protocol (either REST or Wire).
Upon doing this, this server instantiates the appropriate transfer protocol API (either RestAPIStub or WireProtocolStub),
which will convert the objects it receives into a centralized internal representation which is shared between the Stubs.
This representation (implemented as a python dictionary) is the internal request object, and is then passed to the
RequestProcessor (also instantiated by the server) at the receipt of each request. The RequestProcessor houses all of the
critical data structures of the server, such as the store of users, groups, messages, etc. 

USAGE: python server.py [rest/wire]
"""

import os
import sys
import pdb
import traceback
from flask import Flask, render_template, request, jsonify
from RestAPIStub import RestAPIStub
from WireProtocolStub import WireProtocolStub
from requestprocessor import RequestProcessor

app = Flask(__name__)
app.debug = True

# Load the apprpriate stub for decoding requests
if sys.argv[1] == 'rest':
    stub = RestAPIStub()
else:
    stub = WireProtocolStub()

request_processor = RequestProcessor()

def process_request(request_object):
    # This maps each request type to a command in the RequestProcessor.
    mapping = {
        "GetMessages"   : request_processor.get_messages,
        "SendMessage"   : request_processor.send_message,
        "ListAccounts"  : request_processor.list_accounts,
        "DeleteAccount" : request_processor.delete_account,
        "CreateUser"    : request_processor.register_user,
        "GetGroups"     : request_processor.list_groups,
        "CreateGroup"   : request_processor.create_group,
    }
    return mapping[request_object["task"]](request_object)

# Catch all urls, and then parse them in the stubs. This allows us to
# implement a REST-style API and the WireProtocol API over HTTP.
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
def catch_all(path):
    try:
        request_object = stub.decode(path, request)
        return_object  = process_request(request_object)
        return stub.encode(return_object), 200
    except Exception,e:
        traceback.print_exc()
        return "failure!" + str(e), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 30978))
    app.run(host='0.0.0.0', port=port)
